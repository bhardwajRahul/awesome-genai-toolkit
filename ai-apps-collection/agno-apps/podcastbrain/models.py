from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Tone(str, Enum):
    CURIOUS = "curious"
    ENTHUSIASTIC = "enthusiastic"
    THOUGHTFUL = "thoughtful"
    SKEPTICAL = "skeptical"
    HUMOROUS = "humorous"
    ANALYTICAL = "analytical"
    PASSIONATE = "passionate"


class PodcastSegment(BaseModel):
    speaker: str = Field(description="Name of the speaker: 'Host' or 'Expert'")
    text: str = Field(description="The spoken dialogue text")
    tone: Tone = Field(description="The emotional tone of this segment")


class HostResponse(BaseModel):
    text: str = Field(description="The host's spoken dialogue — a question, comment, or reaction")
    tone: Tone = Field(description="The emotional tone")


class ExpertResponse(BaseModel):
    text: str = Field(description="The expert's spoken dialogue — an answer, insight, or counterpoint")
    tone: Tone = Field(description="The emotional tone")


class EpisodeSummary(BaseModel):
    summary: str = Field(description="A 2-3 sentence summary of the episode")
    key_takeaways: list[str] = Field(description="3-5 key takeaways from the conversation")
    topics_covered: list[str] = Field(description="List of specific topics discussed")


class UserPreferences(BaseModel):
    liked_topics: list[str] = Field(default_factory=list, description="Topics the user enjoyed")
    disliked_topics: list[str] = Field(default_factory=list, description="Topics the user didn't enjoy")
    knowledge_level: str = Field(default="intermediate", description="beginner, intermediate, or advanced")
    preferred_depth: str = Field(default="balanced", description="surface, balanced, or deep-dive")
    preferred_tone: str = Field(default="conversational", description="casual, conversational, or academic")
