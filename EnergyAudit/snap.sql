-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: energyaudit
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.10.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `EAComp`
--

DROP TABLE IF EXISTS `EAComp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EAComp` (
  `DID` int(11) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL,
  `Ports` varchar(255) DEFAULT NULL,
  `Position` varchar(255) DEFAULT NULL,
  `Version` varchar(255) DEFAULT NULL,
  `Snap` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EAComp`
--

LOCK TABLES `EAComp` WRITE;
/*!40000 ALTER TABLE `EAComp` DISABLE KEYS */;
INSERT INTO `EAComp` VALUES (41,'','ppcost','','','','','',0.5),(42,'','BVI1','','','','','',0),(42,'','Management0/0','','','','','',0),(42,'','Redundant1.2028','','','','','',0),(42,'','Redundant1.3028','','','','','',0),(43,'','WS-X6716-10GE','','','','','',0),(43,'','WS-SUP720-3BXL','','','','','',0),(43,'','WS-X6716-10GE','','','','','',0),(43,'','TenGigabitEthernet1/1','','','','','',0),(43,'','TenGigabitEthernet1/2','','','','','',0),(43,'','TenGigabitEthernet1/3','','','','','',0),(43,'','TenGigabitEthernet1/4','','','','','',0),(43,'','TenGigabitEthernet1/5','','','','','',0),(43,'','TenGigabitEthernet1/6','','','','','',0),(43,'','TenGigabitEthernet1/7','','','','','',0),(43,'','TenGigabitEthernet1/8','','','','','',0),(43,'','TenGigabitEthernet1/9','','','','','',0),(43,'','TenGigabitEthernet1/10','','','','','',0),(43,'','TenGigabitEthernet1/11','','','','','',0),(43,'','TenGigabitEthernet1/12','','','','','',0),(43,'','TenGigabitEthernet1/13','','','','','',0),(43,'','TenGigabitEthernet1/14','','','','','',0),(43,'','TenGigabitEthernet1/15','','','','','',0),(43,'','TenGigabitEthernet1/16','','','','','',0),(43,'','GigabitEthernet5/1','','','','','',0),(43,'','GigabitEthernet5/2','','','','','',0),(43,'','TenGigabitEthernet9/1','','','','','',0),(43,'','TenGigabitEthernet9/2','','','','','',0),(43,'','TenGigabitEthernet9/3','','','','','',0),(43,'','TenGigabitEthernet9/4','','','','','',0),(43,'','TenGigabitEthernet9/5','','','','','',0),(43,'','TenGigabitEthernet9/6','','','','','',0),(43,'','TenGigabitEthernet9/7','','','','','',0),(43,'','TenGigabitEthernet9/8','','','','','',0),(43,'','TenGigabitEthernet9/9','','','','','',0),(43,'','TenGigabitEthernet9/10','','','','','',0),(43,'','TenGigabitEthernet9/11','','','','','',0),(43,'','TenGigabitEthernet9/12','','','','','',0),(43,'','TenGigabitEthernet9/13','','','','','',0),(43,'','TenGigabitEthernet9/14','','','','','',0),(43,'','TenGigabitEthernet9/15','','','','','',0),(43,'','TenGigabitEthernet9/16','','','','','',0),(44,'','WS-X6716-10GE','','','','','',0),(44,'','WS-SUP720-3BXL','','','','','',0),(44,'','WS-X6716-10GE','','','','','',0),(44,'','TenGigabitEthernet1/1','','','','','',0),(44,'','TenGigabitEthernet1/2','','','','','',0),(44,'','TenGigabitEthernet1/3','','','','','',0),(44,'','TenGigabitEthernet1/4','','','','','',0),(44,'','TenGigabitEthernet1/5','','','','','',0),(44,'','TenGigabitEthernet1/6','','','','','',0),(44,'','TenGigabitEthernet1/7','','','','','',0),(44,'','TenGigabitEthernet1/8','','','','','',0),(44,'','TenGigabitEthernet1/9','','','','','',0),(44,'','TenGigabitEthernet1/10','','','','','',0),(44,'','TenGigabitEthernet1/11','','','','','',0),(44,'','TenGigabitEthernet1/12','','','','','',0),(44,'','TenGigabitEthernet1/13','','','','','',0),(44,'','TenGigabitEthernet1/14','','','','','',0),(44,'','TenGigabitEthernet1/15','','','','','',0),(44,'','TenGigabitEthernet1/16','','','','','',0),(44,'','GigabitEthernet5/1','','','','','',0),(44,'','GigabitEthernet5/2','','','','','',0),(44,'','TenGigabitEthernet9/1','','','','','',0),(44,'','TenGigabitEthernet9/2','','','','','',0),(44,'','TenGigabitEthernet9/3','','','','','',0),(44,'','TenGigabitEthernet9/4','','','','','',0),(44,'','TenGigabitEthernet9/5','','','','','',0),(44,'','TenGigabitEthernet9/6','','','','','',0),(44,'','TenGigabitEthernet9/7','','','','','',0),(44,'','TenGigabitEthernet9/8','','','','','',0),(44,'','TenGigabitEthernet9/9','','','','','',0),(44,'','TenGigabitEthernet9/10','','','','','',0),(44,'','TenGigabitEthernet9/11','','','','','',0),(44,'','TenGigabitEthernet9/12','','','','','',0),(44,'','TenGigabitEthernet9/13','','','','','',0),(44,'','TenGigabitEthernet9/14','','','','','',0),(44,'','TenGigabitEthernet9/15','','','','','',0),(44,'','TenGigabitEthernet9/16','','','','','',0),(45,'','Embedded-Service-Engine0/0','','','','','',0),(45,'','GigabitEthernet0/0','','','','','',0),(45,'','GigabitEthernet0/1','','','','','',0),(45,'','GigabitEthernet0/2','','','','','',0),(45,'','Async0/0/0','','','','','',0),(45,'','Async0/1/0','','','','','',0),(45,'','Async0/0/1','','','','','',0),(45,'','Async0/1/1','','','','','',0),(45,'','Async0/0/2','','','','','',0),(45,'','Async0/1/2','','','','','',0),(45,'','Async0/0/3','','','','','',0),(45,'','Async0/1/3','','','','','',0),(45,'','Async0/0/4','','','','','',0),(45,'','Async0/1/4','','','','','',0),(45,'','Async0/0/5','','','','','',0),(45,'','Async0/1/5','','','','','',0),(45,'','Async0/0/6','','','','','',0),(45,'','Async0/1/6','','','','','',0),(45,'','Async0/0/7','','','','','',0),(45,'','Async0/1/7','','','','','',0),(45,'','Async0/0/8','','','','','',0),(45,'','Async0/1/8','','','','','',0),(45,'','Async0/0/9','','','','','',0),(45,'','Async0/1/9','','','','','',0),(45,'','Async0/0/10','','','','','',0),(45,'','Async0/1/10','','','','','',0),(45,'','Async0/0/11','','','','','',0),(45,'','Async0/1/11','','','','','',0),(45,'','Async0/0/12','','','','','',0),(45,'','Async0/1/12','','','','','',0),(45,'','Async0/0/13','','','','','',0),(45,'','Async0/1/13','','','','','',0),(45,'','Async0/0/14','','','','','',0),(45,'','Async0/1/14','','','','','',0),(45,'','Async0/0/15','','','','','',0),(45,'','Async0/1/15','','','','','',0),(46,'','Null0','','','','','',0),(46,'','GigabitEthernet0/0','','','','','',0),(46,'','GigabitEthernet0/1','','','','','',0),(47,'','GigabitEthernet0/0','','','','','',0),(47,'','GigabitEthernet0/1','','','','','',0),(47,'','GigabitEthernet0/2','','','','','',0),(47,'','GigabitEthernet0/3','','','','','',0),(47,'','Management0/0','','','','','',0),(47,'','Redundant1','','','','','',0),(48,'','ppcost','','','','','',0.3),(49,'','ppcost','','','','','',0.27),(50,'','ppcost','','','','','',0.7887),(52,'','ppcost','','','','','',0.14),(53,'','ppcost','','','','','',1.6),(54,'','ppcost','','','','','',0.14),(55,'','ppcost','','','','','',1.7),(56,'','ppcost','','','','','',0.5),(57,'','ppcost','','','','','',0.5);
/*!40000 ALTER TABLE `EAComp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EADevice`
--

DROP TABLE IF EXISTS `EADevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EADevice` (
  `DID` int(11) DEFAULT NULL,
  `DevManufacturer` varchar(255) DEFAULT NULL,
  `DevType` varchar(255) DEFAULT NULL,
  `Snap` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EADevice`
--

LOCK TABLES `EADevice` WRITE;
/*!40000 ALTER TABLE `EADevice` DISABLE KEYS */;
INSERT INTO `EADevice` VALUES (41,'cisco','WS-C3750X-48',91.4),(42,'cisco','ASA5580-40',503.6),(43,'cisco','WS-C6509-V-E',1019.7),(44,'cisco','WS-C6509-V-E',1019.7),(45,'cisco','CISCO2921/K9',59.1),(46,'cisco','3845',71.3),(47,'cisco','ASA5520',14.4),(48,'cisco','WS-C3550-48',61.22),(49,'cisco','WS-C3550-24',37.87),(50,'cisco','WS-C3750G-48TS',79),(51,'cisco','WS-C6506',277.687),(52,'cisco','WS-C3750G-12S',42.26),(53,'cisco','WS-C3750E-48TD',84.14),(54,'cisco','WS-C3750-48TS',41.14),(55,'cisco','WS-C3750G-24TS',75.3),(56,'cisco','WS-C3750X-48T',96.9),(57,'cisco','WS-C3750X-48P',96.9);
/*!40000 ALTER TABLE `EADevice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-06-27 22:31:23
