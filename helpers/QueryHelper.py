class QueryHelper():

    def checkQueryLimit(query, data):
        limit = data.get('limit')
        if limit:
            query = query.limit(limit)
        return query

    def checkQueryOffset(query, data):
        offset = data.get('offset')
        if offset:
            query = query.offset(offset)
        return query
