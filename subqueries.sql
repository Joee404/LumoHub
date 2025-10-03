-- 1. Users table is already handled by Django auth_user

-- 2. Watchlist
CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    movie_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'to_watch',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Favorites
CREATE TABLE favorite (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    movie_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. WatchedHistory
CREATE TABLE watched_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    movie_id VARCHAR(50) NOT NULL,
    user_rating INTEGER,
    user_review TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. UserPreference
CREATE TABLE user_preference (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    liked_genres VARCHAR(200) NOT NULL,
    disliked_genres VARCHAR(200) NOT NULL,
    liked_actors VARCHAR(200),
    disliked_actors VARCHAR(200),
    preferred_age_rating VARCHAR(10) NOT NULL,
    preferred_content_type VARCHAR(20) NOT NULL DEFAULT 'Movies',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Recommendation
CREATE TABLE recommendation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    movie_id VARCHAR(50) NOT NULL,
    source VARCHAR(50) NOT NULL,
    context VARCHAR(200),
    confidence_score REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. UserQuery
CREATE TABLE user_query (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    response_summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes (optional but recommended for faster queries)
CREATE INDEX idx_watchlist_user ON watchlist(user_id);
CREATE INDEX idx_favorite_user ON favorite(user_id);
CREATE INDEX idx_watched_history_user ON watched_history(user_id);
CREATE INDEX idx_user_preference_user ON user_preference(user_id);
CREATE INDEX idx_recommendation_user ON recommendation(user_id);
CREATE INDEX idx_user_query_user ON user_query(user_id);
