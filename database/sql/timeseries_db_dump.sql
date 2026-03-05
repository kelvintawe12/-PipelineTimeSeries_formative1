-- MySQL dump 10.13  Distrib 8.4.8, for Win64 (x86_64)
--
-- Host: localhost    Database: timeseries_db
-- ------------------------------------------------------
-- Server version	8.4.8

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assets` (
  `asset_id` int NOT NULL AUTO_INCREMENT,
  `asset_name` varchar(100) NOT NULL,
  `asset_type` enum('equity','bond','commodity','crypto','index') NOT NULL,
  `ticker_symbol` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`asset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets`
--

LOCK TABLES `assets` WRITE;
/*!40000 ALTER TABLE `assets` DISABLE KEYS */;
INSERT INTO `assets` VALUES (1,'US Equities','equity','SPY','2026-03-04 18:20:24'),(2,'Technology Stocks','equity','XLK','2026-03-04 18:20:24'),(3,'Emerging Markets','equity','EEM','2026-03-04 18:20:24'),(4,'Long-Term Bonds','bond','TLT','2026-03-04 18:20:24'),(5,'Gold','commodity','GLD','2026-03-04 18:20:24'),(6,'Crude Oil','commodity','USO','2026-03-04 18:20:24'),(7,'Bitcoin','crypto','BTC','2026-03-04 18:20:24');
/*!40000 ALTER TABLE `assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `market_data`
--

DROP TABLE IF EXISTS `market_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `market_data` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `equities_us` decimal(10,2) DEFAULT NULL,
  `equities_tech` decimal(10,2) DEFAULT NULL,
  `equities_emerging` decimal(10,2) DEFAULT NULL,
  `bonds_longterm` decimal(10,2) DEFAULT NULL,
  `gold` decimal(10,2) DEFAULT NULL,
  `oil` decimal(10,2) DEFAULT NULL,
  `volatility_index` decimal(10,2) DEFAULT NULL,
  `crypto_bitcoin` decimal(12,2) DEFAULT NULL,
  `yield_curve_spread` decimal(10,2) DEFAULT NULL,
  `high_yield_spread` decimal(10,2) DEFAULT NULL,
  `financial_stress_index` decimal(10,4) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`record_id`),
  KEY `idx_date` (`date`),
  KEY `idx_financial_stress` (`financial_stress_index`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_data`
--

LOCK TABLES `market_data` WRITE;
/*!40000 ALTER TABLE `market_data` DISABLE KEYS */;
INSERT INTO `market_data` VALUES (1,'2026-02-19',668.00,595.50,60.25,88.50,470.00,79.50,19.20,62000.00,0.55,2.80,-0.5950,'2026-03-04 18:20:24'),(2,'2026-02-20',670.50,598.00,60.80,88.75,471.50,79.80,19.50,62500.00,0.56,2.82,-0.6000,'2026-03-04 18:20:24'),(3,'2026-02-21',675.00,602.00,61.50,89.00,473.00,80.00,19.80,63000.00,0.57,2.83,-0.6050,'2026-03-04 18:20:24'),(4,'2026-02-22',678.20,605.00,62.00,89.50,474.00,80.50,20.00,63500.00,0.58,2.85,-0.6100,'2026-03-04 18:20:24'),(5,'2026-02-23',680.50,607.00,62.30,89.75,474.50,80.60,20.50,64000.00,0.59,2.88,-0.6150,'2026-03-04 18:20:24'),(6,'2026-02-24',682.39,607.50,62.50,89.85,474.55,80.70,21.01,64616.74,0.60,2.90,-0.6180,'2026-03-04 18:20:24'),(7,'2026-02-25',687.35,607.87,62.62,89.90,474.61,80.76,19.55,65568.49,0.61,2.95,-0.6208,'2026-03-04 18:20:24'),(8,'2026-03-05',0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.0000,'2026-03-05 08:15:50');
/*!40000 ALTER TABLE `market_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predictions`
--

DROP TABLE IF EXISTS `predictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predictions` (
  `prediction_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `predicted_value` decimal(10,4) DEFAULT NULL,
  `actual_value` decimal(10,4) DEFAULT NULL,
  `prediction_error` decimal(10,4) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prediction_id`),
  KEY `idx_model` (`model_name`),
  KEY `idx_prediction_date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predictions`
--

LOCK TABLES `predictions` WRITE;
/*!40000 ALTER TABLE `predictions` DISABLE KEYS */;
INSERT INTO `predictions` VALUES (1,'2026-02-25','RandomForest',-0.0472,-0.0450,0.0022,'2026-03-04 18:20:31'),(2,'2026-02-24','RandomForest',-0.0350,-0.0320,0.0030,'2026-03-04 18:20:31'),(3,'2026-02-23','LinearRegression',-0.0280,-0.0300,-0.0020,'2026-03-04 18:20:31');
/*!40000 ALTER TABLE `predictions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-05 11:22:41
