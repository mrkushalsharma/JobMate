sCREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    username VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN
);

CREATE INDEX ix_users_id ON users(id);
CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_users_username ON users(username);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    company VARCHAR,
    description TEXT,
    status VARCHAR,
    application_date TIMESTAMP,
    owner_id INTEGER REFERENCES users(id)
);

CREATE INDEX ix_jobs_id ON jobs(id);
CREATE INDEX ix_jobs_title ON jobs(title);
CREATE INDEX ix_jobs_company ON jobs(company);

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    file_path VARCHAR,
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    owner_id INTEGER REFERENCES users(id)
);

CREATE INDEX ix_resumes_id ON resumes(id);
CREATE INDEX ix_resumes_title ON resumes(title);

CREATE TABLE job_resume_association (
    job_id INTEGER REFERENCES jobs(id),
    resume_id INTEGER REFERENCES resumes(id)
);

CREATE TABLE match_scores (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    job_id INTEGER REFERENCES jobs(id),
    score FLOAT,
    created_at TIMESTAMP
);

CREATE INDEX ix_match_scores_id ON match_scores(id);
