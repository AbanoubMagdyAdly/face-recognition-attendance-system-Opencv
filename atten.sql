-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 18, 2018 at 11:48 AM
-- Server version: 5.7.19
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `atten`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
CREATE TABLE IF NOT EXISTS `attendance` (
  `sid` varchar(15) NOT NULL,
  `sname` varchar(30) NOT NULL,
  `secid` int(15) NOT NULL,
  `atten` int(10) NOT NULL DEFAULT '0',
  `date` varchar(20) NOT NULL DEFAULT '2018-5-10',
  PRIMARY KEY (`sid`,`secid`),
  UNIQUE KEY `sid` (`sid`,`secid`),
  KEY `secid` (`secid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`sid`, `sname`, `secid`, `atten`, `date`) VALUES
('1', 'bino', 3, 8, '2018-05-11'),
('1252', ',mmmm,', 1, 0, '2018-5-10'),
('55', 'bino', 3, 1, '2018-05-12');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `did` int(15) NOT NULL,
  `dname` text NOT NULL,
  `dpass` varchar(15) NOT NULL,
  `dtype` char(1) NOT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`did`, `dname`, `dpass`, `dtype`) VALUES
(1, 'mark', '123', 'a'),
(2, 'poppa', '123', 'd'),
(3, 'Ahmed Saleh', '123', 'a'),
(4, 'Menna Elmasry', '123', 'a'),
(6, 'Youstina Nabil', '123', 'a'),
(7, 'Sara Saad', '123', 'a'),
(8, 'Sara Anwar', '123', 'a'),
(9, 'Ahmed Saleh', '123', 'a'),
(10, 'Menna Elmasry', '123', 'a'),
(11, 'Youstina Nabil', '123', 'a'),
(12, 'Sara Saad', '123', 'a'),
(13, 'Sara Anwar', '123', 'a');

-- --------------------------------------------------------

--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section` (
  `secid` int(3) NOT NULL AUTO_INCREMENT,
  `coursecode` text NOT NULL,
  `labid` char(1) NOT NULL,
  `time` int(6) NOT NULL,
  `day` varchar(8) NOT NULL,
  `did` int(15) NOT NULL,
  PRIMARY KEY (`secid`),
  UNIQUE KEY `section_unique` (`time`,`day`,`labid`),
  KEY `did` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`secid`, `coursecode`, `labid`, `time`, `day`, `did`) VALUES
(1, 'CS102', 'A', 2, 'sat', 1),
(2, 'CS206', 'B', 8, 'wed', 7),
(3, 'CS202', 'C', 2, 'tues', 6),
(5, 'CS212', 'A', 8, 'wed', 3);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student` (
  `sid` varchar(15) NOT NULL,
  `sname` text NOT NULL,
  `autoid` int(4) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`sid`),
  UNIQUE KEY `autoid` (`autoid`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`sid`, `sname`, `autoid`) VALUES
('1', 'bino', 32),
('1252', ',mmmm,', 34),
('55', 'bino', 33);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `secid-fk` FOREIGN KEY (`secid`) REFERENCES `section` (`secid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sid_fk` FOREIGN KEY (`sid`) REFERENCES `student` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `section`
--
ALTER TABLE `section`
  ADD CONSTRAINT `did_fk` FOREIGN KEY (`did`) REFERENCES `doctor` (`did`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
