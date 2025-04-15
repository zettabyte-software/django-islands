class BaseIslandError(Exception):
    pass


class EmptyTenantError(BaseIslandError):
    pass


class ChangeTenantError(BaseIslandError):
    pass
