"""
Database storage system for the Deixis AI Agent.
"""

import sqlite3
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from models.schemas import LLMResponse, AnnotatedResponse, BatchExperiment, ExperimentResults
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages SQLite database operations for storing responses and experiments.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self.db_dir = Path(self.db_path).parent
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        self._initialize_database()
        logger.info(f"Database initialized at {self.db_path}")
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Responses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_type TEXT NOT NULL,
                    dilemma_id TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    token_count INTEGER DEFAULT 0,
                    processing_time REAL DEFAULT 0.0,
                    temperature REAL DEFAULT 0.7,
                    max_tokens INTEGER DEFAULT 2000
                )
            """)
            
            # Annotations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS annotations (
                    response_id TEXT PRIMARY KEY,
                    linguistic_annotation TEXT,
                    ethical_annotation TEXT,
                    manual_annotations TEXT,
                    annotation_timestamp TEXT,
                    annotator_id TEXT,
                    FOREIGN KEY (response_id) REFERENCES responses (id)
                )
            """)
            
            # Experiments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    dilemma_ids TEXT NOT NULL,
                    framing_types TEXT NOT NULL,
                    models TEXT NOT NULL,
                    runs_per_combination INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            """)
            
            # Experiment results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_results (
                    experiment_id TEXT PRIMARY KEY,
                    total_responses INTEGER,
                    completed_responses INTEGER,
                    failed_responses INTEGER,
                    average_processing_time REAL,
                    stance_distribution TEXT,
                    framing_effectiveness TEXT,
                    model_comparison TEXT,
                    generated_at TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES experiments (id)
                )
            """)
            
            conn.commit()
            logger.info("Database tables initialized")
    
    def store_response(self, response: LLMResponse) -> bool:
        """
        Store an LLM response in the database.
        
        Args:
            response: LLMResponse object to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO responses 
                    (id, timestamp, model, prompt_type, dilemma_id, prompt_text, 
                     response_text, token_count, processing_time, temperature, max_tokens)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    response.id,
                    response.timestamp.isoformat(),
                    response.model.value,
                    response.prompt_type.value,
                    response.dilemma_id,
                    response.prompt_text,
                    response.response_text,
                    response.token_count,
                    response.processing_time,
                    response.temperature,
                    response.max_tokens
                ))
                
                conn.commit()
                logger.info(f"Stored response {response.id}")
                return True
                
        except Exception as e:
            logger.error(f"Error storing response {response.id}: {e}")
            return False
    
    def store_annotation(self, annotated_response: AnnotatedResponse) -> bool:
        """
        Store an annotated response in the database.
        
        Args:
            annotated_response: AnnotatedResponse object to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First store the base response
            if not self.store_response(annotated_response.response):
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO annotations 
                    (response_id, linguistic_annotation, ethical_annotation, 
                     manual_annotations, annotation_timestamp, annotator_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    annotated_response.response.id,
                    json.dumps(annotated_response.linguistic_annotation.dict()),
                    json.dumps(annotated_response.ethical_annotation.dict()),
                    json.dumps(annotated_response.manual_annotations),
                    annotated_response.annotation_timestamp.isoformat(),
                    annotated_response.annotator_id
                ))
                
                conn.commit()
                logger.info(f"Stored annotation for response {annotated_response.response.id}")
                return True
                
        except Exception as e:
            logger.error(f"Error storing annotation: {e}")
            return False
    
    def get_response(self, response_id: str) -> Optional[LLMResponse]:
        """
        Retrieve a response by ID.
        
        Args:
            response_id: ID of the response to retrieve
            
        Returns:
            LLMResponse object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM responses WHERE id = ?
                """, (response_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                # Convert row to LLMResponse
                return self._row_to_response(row)
                
        except Exception as e:
            logger.error(f"Error retrieving response {response_id}: {e}")
            return None
    
    def get_responses_by_dilemma(self, dilemma_id: str) -> List[LLMResponse]:
        """
        Get all responses for a specific dilemma.
        
        Args:
            dilemma_id: ID of the dilemma
            
        Returns:
            List of LLMResponse objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM responses WHERE dilemma_id = ?
                    ORDER BY timestamp DESC
                """, (dilemma_id,))
                
                rows = cursor.fetchall()
                return [self._row_to_response(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error retrieving responses for dilemma {dilemma_id}: {e}")
            return []
    
    def get_responses_by_framing(self, framing_type: str) -> List[LLMResponse]:
        """
        Get all responses for a specific framing type.
        
        Args:
            framing_type: Type of deictic framing
            
        Returns:
            List of LLMResponse objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM responses WHERE prompt_type = ?
                    ORDER BY timestamp DESC
                """, (framing_type,))
                
                rows = cursor.fetchall()
                return [self._row_to_response(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error retrieving responses for framing {framing_type}: {e}")
            return []
    
    def store_experiment(self, experiment: BatchExperiment) -> bool:
        """
        Store a batch experiment configuration.
        
        Args:
            experiment: BatchExperiment object to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO experiments 
                    (id, name, description, dilemma_ids, framing_types, models,
                     runs_per_combination, created_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    experiment.id,
                    experiment.name,
                    experiment.description,
                    json.dumps(experiment.dilemma_ids),
                    json.dumps([f.value for f in experiment.framing_types]),
                    json.dumps([m.value for m in experiment.models]),
                    experiment.runs_per_combination,
                    experiment.created_at.isoformat(),
                    experiment.status
                ))
                
                conn.commit()
                logger.info(f"Stored experiment {experiment.id}")
                return True
                
        except Exception as e:
            logger.error(f"Error storing experiment {experiment.id}: {e}")
            return False
    
    def get_experiment_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count responses
                cursor.execute("SELECT COUNT(*) FROM responses")
                total_responses = cursor.fetchone()[0]
                
                # Count annotations
                cursor.execute("SELECT COUNT(*) FROM annotations")
                total_annotations = cursor.fetchone()[0]
                
                # Count experiments
                cursor.execute("SELECT COUNT(*) FROM experiments")
                total_experiments = cursor.fetchone()[0]
                
                # Get unique dilemmas
                cursor.execute("SELECT COUNT(DISTINCT dilemma_id) FROM responses")
                unique_dilemmas = cursor.fetchone()[0]
                
                # Get unique models
                cursor.execute("SELECT COUNT(DISTINCT model) FROM responses")
                unique_models = cursor.fetchone()[0]
                
                return {
                    "total_responses": total_responses,
                    "total_annotations": total_annotations,
                    "total_experiments": total_experiments,
                    "unique_dilemmas": unique_dilemmas,
                    "unique_models": unique_models,
                    "database_path": self.db_path
                }
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def _row_to_response(self, row) -> LLMResponse:
        """Convert database row to LLMResponse object."""
        from models.schemas import LLMModel, DeicticFraming
        
        return LLMResponse(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            model=LLMModel(row[2]),
            prompt_type=DeicticFraming(row[3]),
            dilemma_id=row[4],
            prompt_text=row[5],
            response_text=row[6],
            token_count=row[7],
            processing_time=row[8],
            temperature=row[9],
            max_tokens=row[10]
        )
    
    def export_to_jsonl(self, output_path: str, include_annotations: bool = True) -> bool:
        """
        Export all data to JSONL format.
        
        Args:
            output_path: Path to output JSONL file
            include_annotations: Whether to include annotation data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import jsonlines
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if include_annotations:
                    query = """
                        SELECT r.*, a.linguistic_annotation, a.ethical_annotation, 
                               a.manual_annotations, a.annotation_timestamp, a.annotator_id
                        FROM responses r
                        LEFT JOIN annotations a ON r.id = a.response_id
                        ORDER BY r.timestamp
                    """
                else:
                    query = "SELECT * FROM responses ORDER BY timestamp"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                with jsonlines.open(output_path, mode='w') as writer:
                    for row in rows:
                        if include_annotations and len(row) > 11:
                            # Include annotation data
                            record = {
                                "response": {
                                    "id": row[0],
                                    "timestamp": row[1],
                                    "model": row[2],
                                    "prompt_type": row[3],
                                    "dilemma_id": row[4],
                                    "prompt_text": row[5],
                                    "response_text": row[6],
                                    "token_count": row[7],
                                    "processing_time": row[8],
                                    "temperature": row[9],
                                    "max_tokens": row[10]
                                },
                                "annotations": {
                                    "linguistic": json.loads(row[11]) if row[11] else None,
                                    "ethical": json.loads(row[12]) if row[12] else None,
                                    "manual": json.loads(row[13]) if row[13] else None,
                                    "timestamp": row[14],
                                    "annotator_id": row[15]
                                }
                            }
                        else:
                            # Response only
                            record = {
                                "id": row[0],
                                "timestamp": row[1],
                                "model": row[2],
                                "prompt_type": row[3],
                                "dilemma_id": row[4],
                                "prompt_text": row[5],
                                "response_text": row[6],
                                "token_count": row[7],
                                "processing_time": row[8],
                                "temperature": row[9],
                                "max_tokens": row[10]
                            }
                        
                        writer.write(record)
                
                logger.info(f"Exported {len(rows)} records to {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"Error exporting to JSONL: {e}")
            return False