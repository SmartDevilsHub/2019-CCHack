-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 14, 2019 at 02:41 PM
-- Server version: 5.7.27-0ubuntu0.19.04.1
-- PHP Version: 7.2.19-0ubuntu0.19.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cchack`
--

-- --------------------------------------------------------

--
-- Table structure for table `device_connections`
--

CREATE TABLE `device_connections` (
  `ID` int(11) NOT NULL,
  `DEV1` int(11) NOT NULL,
  `DEV2` int(11) NOT NULL,
  `DIST` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Connections between devices';

--
-- Dumping data for table `device_connections`
--

INSERT INTO `device_connections` (`ID`, `DEV1`, `DEV2`, `DIST`) VALUES
(1, 2, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `device_table`
--

CREATE TABLE `device_table` (
  `ID` int(11) NOT NULL COMMENT 'Auto Key',
  `IP` varchar(40) NOT NULL COMMENT 'IP of Pi',
  `MAC_Addr` varchar(20) DEFAULT NULL COMMENT 'Device MAC Address',
  `Lat` double DEFAULT NULL COMMENT 'Latitude of device',
  `Lon` double DEFAULT NULL COMMENT 'Longitude of device',
  `PORT` int(11) DEFAULT NULL COMMENT 'PORT Value'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Table for CCHack software';

--
-- Dumping data for table `device_table`
--

INSERT INTO `device_table` (`ID`, `IP`, `MAC_Addr`, `Lat`, `Lon`, `PORT`) VALUES
(1, '255.255.255.255', 'MAC_ADDR', 50.867612, -1.360941, 8880),
(2, '255.255.255.255', 'MAC_ADDR', 68, 421, 23527);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `device_connections`
--
ALTER TABLE `device_connections`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `device_table`
--
ALTER TABLE `device_table`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `device_connections`
--
ALTER TABLE `device_connections`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `device_table`
--
ALTER TABLE `device_table`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Auto Key', AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
