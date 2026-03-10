"""
ML Module — AI-Based Syntax Error Classification & Intelligent Diagnostics

Sub-modules:
  ast_feature_extractor  – Extract structural + contextual features from AST/tokens
  train_classifier       – Train the full ML pipeline (classifier + regressors)
  intelligent_diagnostics– Runtime diagnostics engine with pattern + fix ranking
  anomaly_detector       – Isolation Forest for detecting risky-but-valid code
  batch_analyzer         – K-Means clustering for cross-file root-cause grouping
  online_learner         – Incremental SGD learning from user feedback
"""
