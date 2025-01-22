from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Configuration of the Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os, sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    """
    A class to manage data ingestion processes, including exporting data from MongoDB,
    saving it to feature stores, and splitting it into training and testing datasets.

    Attributes:
        data_ingestion_config (DataIngestionConfig): Configuration for data ingestion processes.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initializes the DataIngestion class with the specified configuration.

        Parameters:
            data_ingestion_config (DataIngestionConfig): Configuration for data ingestion, 
                                                         including database, collection, and file paths.

        Raises:
            NetworkSecurityException: If an error occurs during initialization.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Exports data from a MongoDB collection as a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the exported data.

        Raises:
            NetworkSecurityException: If an error occurs during the data export process.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Exports a DataFrame into a feature store as a CSV file.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to be saved to the feature store.

        Returns:
            pd.DataFrame: The same DataFrame that was saved.

        Raises:
            NetworkSecurityException: If an error occurs while saving the DataFrame.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Creating Folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Splits the data into training and testing sets and saves them to specified file paths.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to be split into train and test sets.

        Raises:
            NetworkSecurityException: If an error occurs during the data split or file export process.
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train-test split on the DataFrame")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file paths.")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info("Exported train and test file paths.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the complete data ingestion process:
        - Exports data from MongoDB.
        - Saves the data to a feature store.
        - Splits the data into training and testing sets.

        Returns:
            DataIngestionArtifact: An artifact containing paths to the train and test datasets.

        Raises:
            NetworkSecurityException: If an error occurs during any part of the data ingestion process.
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
