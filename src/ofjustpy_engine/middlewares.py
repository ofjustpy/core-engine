class DBSessionMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":  # Ensure we're only handling HTTP requests
            request = Request(scope, receive, send)
            # Create an async session for the request
            request.state.db_sessionlocal = sessionmaker(bind=engine,
                                                          class_=AsyncSession,
                                                          expire_on_commit=False,
                                                          )

            try:
                # Call the next middleware or the route handler
                await self.app(scope, receive, send)
                # Commit session if no errors occur
                await request.state.db_sessionlocal.commit()
            except SQLAlchemyError:
                # Rollback the session if an error occurs
                await request.state.db_sessionlocal.rollback()
                raise
            finally:
                # Ensure the session is closed after processing the request
                await request.state.db_sessionlocal.close()
        else:
            # If not HTTP, just pass through
            await self.app(scope, receive, send)
