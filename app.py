# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Question system routes
from routes.generate import router as generate_router
from routes.pdf import router as pdf_router
from routes.analytics import router as analytics_router
from routes.dashboard_router import router as dashboard_router
from routes.feedback_router import router as feedback_router

# Authentication routes
from auth.auth_routes import router as auth_router
from auth.profile_routes import router as profile_router


app = FastAPI(title="Automatic Question Generator")


# Include routers
app.include_router(auth_router)
app.include_router(profile_router)

app.include_router(generate_router)
app.include_router(pdf_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)
app.include_router(feedback_router)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)