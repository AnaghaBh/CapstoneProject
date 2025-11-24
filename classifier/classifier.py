"""DistilBERT classifier for misinformation framework classification."""

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import Dataset
from typing import Dict, Any
from .config import Config

class MisinformationClassifier:
    """DistilBERT-based classifier for psychological misinformation frameworks."""
    
    def __init__(self, framework: str = None, model_name: str = None):
        """Initialize the classifier.
        
        Args:
            framework: Psychological framework to use (elm, schema, fuzzy_trace)
            model_name: Name of the pre-trained model to use
        """
        self.framework = framework or Config.DEFAULT_FRAMEWORK
        self.framework_config = Config.FRAMEWORKS[self.framework]
        self.model_name = model_name or Config.MODEL_NAME
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.framework_config["num_labels"]
        )
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
    
    def tokenize_function(self, examples: Dict[str, Any]) -> Dict[str, Any]:
        """Tokenize input texts."""
        return self.tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=Config.MAX_LENGTH
        )
    
    def prepare_datasets(self, train_dataset: Dataset, val_dataset: Dataset) -> tuple:
        """Tokenize and prepare datasets for training."""
        train_tokenized = train_dataset.map(self.tokenize_function, batched=True)
        val_tokenized = val_dataset.map(self.tokenize_function, batched=True)
        
        return train_tokenized, val_tokenized
    
    def train(self, train_dataset: Dataset, val_dataset: Dataset, output_dir: str = "./results"):
        """Train the classifier."""
        train_tokenized, val_tokenized = self.prepare_datasets(train_dataset, val_dataset)
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=Config.NUM_EPOCHS,
            per_device_train_batch_size=Config.BATCH_SIZE,
            per_device_eval_batch_size=Config.BATCH_SIZE,
            warmup_steps=Config.WARMUP_STEPS,
            weight_decay=Config.WEIGHT_DECAY,
            learning_rate=Config.LEARNING_RATE,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_tokenized,
            eval_dataset=val_tokenized,
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
        )
        
        trainer.train()
        return trainer
    
    def predict(self, texts: list) -> list:
        """Make predictions on new texts."""
        inputs = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=Config.MAX_LENGTH,
            return_tensors="pt"
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_classes = torch.argmax(predictions, dim=-1)
        
        return predicted_classes.tolist()
    
    def save_model(self, path: str):
        """Save the trained model."""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
    
    def load_model(self, path: str):
        """Load a trained model."""
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)