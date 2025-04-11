from fastapi import FastAPI
from backend.api.models import TraceCreate, TraceResponse
from backend.hosting import container
from lagom.integrations.fast_api import FastApiIntegration
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from backend.db.models import AIModelConfig, Trace, Base, User

# TODO: Introduce DB migrations
Base.metadata.drop_all(bind=container[Engine])
Base.metadata.create_all(bind=container[Engine])

app = FastAPI()
deps = FastApiIntegration(container)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/traces", statuse_code=201)
async def traces(
    trace: TraceCreate, session_maker=deps.depends(Session)
) -> TraceResponse:
    with session_maker() as session:
        # TODO: This is a short term helper to manage the data difference
        user = session.query(User).filter_by(username=trace.user.username).first()
        if not user:
            user = User(**trace.user.model_dump())
            session.add(user)
        ai_model_config = (
            session.query(AIModelConfig)
            .filter_by(name=trace.ai_model_config.name)
            .first()
        )
        if not ai_model_config:
            ai_model_config = AIModelConfig(**trace.ai_model_config.model_dump())
            session.add(ai_model_config)
        trace_dict = trace.model_dump()
        trace_dict["user"] = user
        trace_dict["ai_model_config"] = ai_model_config
        trace_db = Trace(**trace_dict)
        session.add(trace_db)
        session.commit()
        session.refresh(trace_db)
        trace_response = TraceResponse.model_validate(trace_db)

    return trace_response
