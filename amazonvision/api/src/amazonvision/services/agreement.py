import sqlite3

from amazonvision.core.clock import to_db, utc_now
from amazonvision.schemas.api import (
    AgreementLabelCreate,
    AgreementLabelOut,
    AgreementQueueItem,
    AgreementSampleResult,
    AgreementSummary,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage import agreement as repo
from amazonvision.storage import dataset as dataset_repo
from amazonvision.storage.db import Database
from amazonvision.storage.products import get_product_row


def _not_found() -> ApiError:
    return ApiError(ErrorCode.NOT_FOUND, "Foto não encontrada.")


class AgreementService:
    """Blind labeling agreement: records each reviewer's own answer, compared only afterwards."""

    def __init__(self, db: Database) -> None:
        self._db = db

    async def _require_product(self, product_id: str) -> None:
        product = await self._db.run(lambda conn: get_product_row(conn, product_id))
        if product is None:
            raise ApiError(ErrorCode.VALIDATION_ERROR, f"Produto {product_id} não existe.")

    async def submit(self, body: AgreementLabelCreate) -> AgreementLabelOut:
        await self._require_product(body.product_id)

        def tx(conn: sqlite3.Connection) -> AgreementLabelOut:
            sample = dataset_repo.get_sample(conn, body.sample_id)
            if sample is None or sample.product_id != body.product_id:
                raise _not_found()
            return repo.upsert_label(
                conn,
                sample_id=body.sample_id,
                session=body.session,
                reviewer=body.reviewer,
                label=body.label,
                at=to_db(utc_now()),
            )

        return await self._db.run(tx)

    async def next(
        self, *, product_id: str, session: str, reviewer: str
    ) -> AgreementQueueItem | None:
        await self._require_product(product_id)
        sample, remaining = await self._db.run(
            lambda conn: repo.next_for_reviewer(
                conn, product_id=product_id, session=session, reviewer=reviewer
            )
        )
        if sample is None:
            return None
        return AgreementQueueItem(sample=sample, remaining=remaining)

    async def summary(self, *, product_id: str, session: str) -> AgreementSummary:
        await self._require_product(product_id)
        rows = await self._db.run(
            lambda conn: repo.samples_with_labels(conn, product_id=product_id, session=session)
        )
        reviewers: set[str] = set()
        compared = 0
        agreed = 0
        disagreements: list[AgreementSampleResult] = []
        for sample, labels in rows:
            reviewers |= labels.keys()
            if len(labels) < 2:
                continue  # only one reviewer has labeled this photo so far: nothing to compare
            compared += 1
            agree = len(set(labels.values())) == 1
            if agree:
                agreed += 1
            else:
                disagreements.append(
                    AgreementSampleResult(sample=sample, labels=labels, agree=False)
                )
        return AgreementSummary(
            product_id=product_id,
            session=session,
            reviewers=sorted(reviewers),
            compared=compared,
            agreed=agreed,
            agreement_rate=(agreed / compared) if compared else None,
            disagreements=disagreements,
        )
