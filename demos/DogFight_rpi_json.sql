-- script to set up MySQL table for pi3d demos/DogFight.py see also
-- rpi_json.php for script to run on server
--
-- phpMyAdmin SQL Dump
-- version 3.5.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 23, 2013 at 07:55 PM
-- Server version: 5.1.68-cll
-- PHP Version: 5.3.17

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `eldwick_ysc`
--

-- --------------------------------------------------------

--
-- Table structure for table `rpi_json`
--

CREATE TABLE IF NOT EXISTS `rpi_json` (
  `id` varchar(36) COLLATE latin1_general_ci NOT NULL,
  `x` float NOT NULL,
  `z` float NOT NULL,
  `tm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `damage` float NOT NULL,
  `json` varchar(2048) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `x` (`x`,`z`),
  KEY `x_2` (`x`,`z`,`tm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
