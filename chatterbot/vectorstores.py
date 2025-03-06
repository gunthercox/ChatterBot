"""
Redis vector store.
"""
from __future__ import annotations

from typing import Any, List, Sequence

from langchain_core.documents import Document
from redisvl.redis.utils import convert_bytes
from redisvl.query import FilterQuery

from langchain_core.documents import Document
from langchain_redis.vectorstores import RedisVectorStore as LangChainRedisVectorStore


class RedisVectorStore(LangChainRedisVectorStore):
    """
    Redis vector store integration.
    """

    def query_search(
        self,
        k=4,
        filter=None,
        sort_by=None,
    ) -> List[Document]:
        """
        Return docs based on the provided query.

        k: int, default=4
            Number of documents to return.
        filter: str, default=None
            A filter expression to apply to the query.
        sort_by: str, default=None
            A field to sort the results by.

        returns:
            A list of Documents most matching the query.
        """
        from chatterbot import ChatBot

        return_fields = [
            self.config.content_field
        ]
        return_fields += [
            field.name
            for field in self._index.schema.fields.values()
            if field.name
            not in [self.config.embedding_field, self.config.content_field]
        ]

        query = FilterQuery(
            return_fields=return_fields,
            num_results=k,
            filter_expression=filter,
            sort_by=sort_by,
        )

        try:
            results = self._index.query(query)
        except Exception as e:
            raise ChatBot.ChatBotException(f'Error querying index: {query}') from e

        if results:
            with self._index.client.pipeline(transaction=False) as pipe:
                for document in results:
                    pipe.hgetall(document['id'])
                full_documents = convert_bytes(pipe.execute())
        else:
            full_documents = []

        return self._prepare_docs_full(
            True, results, full_documents, True
        )
