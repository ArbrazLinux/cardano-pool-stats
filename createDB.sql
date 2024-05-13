CREATE DATABASE IF NOT EXISTS `pool_DB` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;
USE `pool_DB`;

-- --------------------------------------------------------

--
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
CREATE TABLE IF NOT EXISTS `assets` (
  `epoch_epoch_number` int NOT NULL,
  `delegator_stake_address` varchar(128) NOT NULL,
  `name` varchar(64) NOT NULL,
  `amount` int NOT NULL DEFAULT '0',
  `policyID` varchar(64) NOT NULL,
  `name_hash` varchar(64) NOT NULL,
  `fingerprint` varchar(64) NOT NULL,
  PRIMARY KEY (`epoch_epoch_number`,`delegator_stake_address`,`fingerprint`) USING BTREE,
  KEY `fk_assets_epoch_idx` (`epoch_epoch_number`),
  KEY `fk_assets_delegator_idx` (`delegator_stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `blocks`
--

DROP TABLE IF EXISTS `blocks`;
CREATE TABLE IF NOT EXISTS `blocks` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `hash` varchar(64) NOT NULL,
  `height` bigint UNSIGNED NOT NULL,
  `absolute_slot` bigint UNSIGNED NOT NULL,
  `epoch_slot` bigint UNSIGNED NOT NULL,
  `time` timestamp NOT NULL,
  `previous_block_hash` varchar(64) NOT NULL,
  `next_block_hash` varchar(64) NOT NULL,
  `tx_count` int UNSIGNED NOT NULL,
  `fees` bigint UNSIGNED NOT NULL,
  `value` bigint UNSIGNED NOT NULL,
  PRIMARY KEY (`epoch_epoch_number`,`hash`),
  KEY `fk_blocks_epoch_idx` (`epoch_epoch_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `bonus`
--

DROP TABLE IF EXISTS `bonus`;
CREATE TABLE IF NOT EXISTS `bonus` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `delegator_stake_address` varchar(128) NOT NULL,
  `amount` bigint UNSIGNED DEFAULT '0',
  `sum` bigint UNSIGNED DEFAULT '0',
  PRIMARY KEY (`epoch_epoch_number`,`delegator_stake_address`),
  KEY `fk_bonus_epoch_idx` (`epoch_epoch_number`),
  KEY `fk_bonus_delegator_idx` (`delegator_stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `delegator`
--

DROP TABLE IF EXISTS `delegator`;
CREATE TABLE IF NOT EXISTS `delegator` (
  `stake_address` varchar(128) NOT NULL,
  `first_epoch` int UNSIGNED DEFAULT '0',
  `since_epoch` int UNSIGNED DEFAULT '0',
  `gone_epoch` int UNSIGNED DEFAULT '0',
  `epoch_count` int UNSIGNED NOT NULL DEFAULT '1',
  `loyalty` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `comeback` tinyint NOT NULL,
  `comeback_count` int UNSIGNED DEFAULT '0',
  `stake` bigint UNSIGNED DEFAULT '0',
  `stake_sum` bigint UNSIGNED DEFAULT '0',
  `stake_previous` bigint UNSIGNED DEFAULT '0',
  `stake_diff` bigint DEFAULT '0',
  `inputs_sum` bigint UNSIGNED DEFAULT '0',
  `outputs_sum` bigint DEFAULT '0',
  `stake_max` bigint UNSIGNED DEFAULT '0',
  `stake_min` bigint UNSIGNED DEFAULT '0',
  `rewards` bigint UNSIGNED DEFAULT '0',
  `rewards_sum` bigint UNSIGNED DEFAULT '0',
  `bonus` bigint UNSIGNED DEFAULT '0',
  `bonus_sum` bigint UNSIGNED DEFAULT '0',
  `ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_bonus_included` decimal(10,2) UNSIGNED DEFAULT '0.00',
  PRIMARY KEY (`stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `epoch`
--

DROP TABLE IF EXISTS `epoch`;
CREATE TABLE IF NOT EXISTS `epoch` (
  `epoch_number` int UNSIGNED NOT NULL,
  `pool_stake` bigint UNSIGNED DEFAULT '0',
  `pool_stake_previous` bigint UNSIGNED DEFAULT '0',
  `pool_stake_sum` bigint UNSIGNED DEFAULT '0',
  `pool_stake_diff` bigint DEFAULT '0',
  `pool_stake_inputs_sum` bigint UNSIGNED DEFAULT '0',
  `pool_stake_outputs_sum` bigint DEFAULT '0',
  `pool_stake_max` bigint UNSIGNED DEFAULT '0',
  `pool_stake_min` bigint UNSIGNED DEFAULT '0',
  `biggest_single_owner_pledge` bigint UNSIGNED DEFAULT '0',
  `biggest_single_delegator_stake` bigint UNSIGNED DEFAULT '0',
  `pool_rewards` bigint UNSIGNED DEFAULT '0',
  `pool_rewards_sum` bigint UNSIGNED DEFAULT '0',
  `pool_ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `pool_ROA_max` decimal(10,2) UNSIGNED DEFAULT NULL,
  `owners_nb` int UNSIGNED NOT NULL DEFAULT '1',
  `pledge` bigint UNSIGNED DEFAULT '0',
  `pledge_previous` bigint UNSIGNED DEFAULT '0',
  `pledge_sum` bigint UNSIGNED DEFAULT '0',
  `pledge_diff` bigint DEFAULT '0',
  `pledge_inputs_sum` bigint UNSIGNED DEFAULT '0',
  `pledge_outputs_sum` bigint DEFAULT '0',
  `pledge_max` bigint UNSIGNED DEFAULT '0',
  `pledge_min` bigint UNSIGNED DEFAULT '0',
  `owners_rewards` bigint UNSIGNED DEFAULT '0',
  `owners_rewards_sum` bigint UNSIGNED DEFAULT '0',
  `owners_ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `owners_ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `delegators_nb` int UNSIGNED DEFAULT '0',
  `delegators_back_count` int UNSIGNED DEFAULT '0',
  `delegators_back_sum` int UNSIGNED DEFAULT '0',
  `delegators_lost_count` int UNSIGNED DEFAULT '0',
  `delegators_lost_sum` int UNSIGNED DEFAULT '0',
  `delegators_stake` bigint UNSIGNED DEFAULT '0',
  `delegators_stake_previous` bigint UNSIGNED DEFAULT '0',
  `delegators_stake_diff` bigint DEFAULT '0',
  `delegators_stake_sum` bigint UNSIGNED DEFAULT '0',
  `delegators_stake_inputs_sum` bigint UNSIGNED DEFAULT '0',
  `delegators_stake_outputs_sum` bigint DEFAULT '0',
  `delegators_stake_max` bigint UNSIGNED DEFAULT '0',
  `delegators_stake_min` bigint UNSIGNED DEFAULT '0',
  `delegators_lost_stake` bigint DEFAULT '0',
  `delegators_lost_stake_sum` bigint DEFAULT '0',
  `delegators_rewards` bigint UNSIGNED DEFAULT '0',
  `delegators_rewards_sum` bigint UNSIGNED DEFAULT '0',
  `delegators_ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `delegators_ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `delegators_ROA_bonusincluded` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `blocks` int UNSIGNED DEFAULT '0',
  `blocks_sum` int UNSIGNED DEFAULT '0',
  `bonuses` bigint UNSIGNED DEFAULT '0',
  `bonuses_sum` bigint UNSIGNED DEFAULT '0',
  PRIMARY KEY (`epoch_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `gone_delegators`
--

DROP TABLE IF EXISTS `gone_delegators`;
CREATE TABLE IF NOT EXISTS `gone_delegators` (
  `delegator_stake_address` varchar(128) NOT NULL,
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `first_epoch` int UNSIGNED NOT NULL DEFAULT '0',
  `since_epoch` int NOT NULL DEFAULT '0',
  `gone_count` int UNSIGNED NOT NULL DEFAULT '1',
  `lost_stake` bigint NOT NULL DEFAULT '0',
  `back_count` int UNSIGNED NOT NULL DEFAULT '0',
  `lost_stake_sum` bigint NOT NULL DEFAULT '0',
  PRIMARY KEY (`delegator_stake_address`,`epoch_epoch_number`,`back_count`) USING BTREE,
  KEY `fk_gone delegators_epoch1_idx` (`epoch_epoch_number`),
  KEY `fk_gone delegators_delegator1_idx` (`delegator_stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
CREATE TABLE IF NOT EXISTS `owner` (
  `stake_address` varchar(128) NOT NULL,
  `first_epoch` int UNSIGNED DEFAULT '0',
  `since_epoch` int UNSIGNED DEFAULT '0',
  `gone_epoch` int UNSIGNED DEFAULT '0',
  `epoch_count` int UNSIGNED DEFAULT '1',
  `loyalty` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `pledge` bigint UNSIGNED DEFAULT '0',
  `pledge_sum` bigint UNSIGNED DEFAULT '0',
  `pledge_previous` bigint UNSIGNED DEFAULT '0',
  `pledge_diff` bigint DEFAULT NULL,
  `pledge_max` bigint UNSIGNED DEFAULT '0',
  `pledge_min` bigint UNSIGNED DEFAULT '0',
  `rewards` bigint UNSIGNED DEFAULT '0',
  `rewards_sum` bigint UNSIGNED DEFAULT '0',
  `inputs_sum` bigint UNSIGNED DEFAULT '0',
  `outputs_sum` bigint DEFAULT '0',
  `ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  PRIMARY KEY (`stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `owner_rewards`
--

DROP TABLE IF EXISTS `owner_rewards`;
CREATE TABLE IF NOT EXISTS `owner_rewards` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `owner_stake_address` varchar(128) NOT NULL,
  `amount` bigint UNSIGNED DEFAULT '0',
  `sum` bigint UNSIGNED DEFAULT '0',
  PRIMARY KEY (`epoch_epoch_number`,`owner_stake_address`),
  KEY `fk_owner_rewards_epoch_idx` (`epoch_epoch_number`),
  KEY `fk_owner_rewards_owner_idx` (`owner_stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `pledge`
--

DROP TABLE IF EXISTS `pledge`;
CREATE TABLE IF NOT EXISTS `pledge` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `owner_stake_address` varchar(128) NOT NULL,
  `amount` bigint UNSIGNED DEFAULT '0',
  `sum` bigint UNSIGNED DEFAULT '0',
  `previous` bigint UNSIGNED DEFAULT '0',
  `diff` bigint DEFAULT '0',
  `inputs_sum` bigint UNSIGNED DEFAULT '0',
  `outputs_sum` bigint DEFAULT '0',
  `max` bigint UNSIGNED DEFAULT '0',
  `min` bigint UNSIGNED DEFAULT '0',
  `ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  PRIMARY KEY (`epoch_epoch_number`,`owner_stake_address`),
  KEY `fk_pledge_epoch_idx` (`epoch_epoch_number`),
  KEY `fk_pledge_owner_idx` (`owner_stake_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `rewards`
--

DROP TABLE IF EXISTS `rewards`;
CREATE TABLE IF NOT EXISTS `rewards` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `delegator_stake_address` varchar(128) NOT NULL,
  `amount` bigint UNSIGNED DEFAULT '0',
  `sum` bigint UNSIGNED DEFAULT '0',
  PRIMARY KEY (`epoch_epoch_number`,`delegator_stake_address`),
  KEY `fk_rewards_delegator_idx` (`delegator_stake_address`),
  KEY `fk_rewards_epoch_idx` (`epoch_epoch_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `stake`
--

DROP TABLE IF EXISTS `stake`;
CREATE TABLE IF NOT EXISTS `stake` (
  `epoch_epoch_number` int UNSIGNED NOT NULL,
  `delegator_stake_address` varchar(128) NOT NULL,
  `amount` bigint UNSIGNED DEFAULT '0',
  `sum` bigint UNSIGNED DEFAULT '0',
  `previous` bigint UNSIGNED DEFAULT '0',
  `diff` bigint DEFAULT '0',
  `inputs_sum` bigint UNSIGNED DEFAULT '0',
  `outputs_sum` bigint DEFAULT '0',
  `max` bigint UNSIGNED DEFAULT '0',
  `min` bigint UNSIGNED DEFAULT '0',
  `ROA_current` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_max` decimal(10,2) UNSIGNED DEFAULT '0.00',
  `ROA_bonusincluded` decimal(10,2) UNSIGNED DEFAULT '0.00',
  PRIMARY KEY (`epoch_epoch_number`,`delegator_stake_address`),
  KEY `fk_stake_delegator_idx` (`delegator_stake_address`),
  KEY `fk_stake_epoch_idx` (`epoch_epoch_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `blocks`
--
ALTER TABLE `blocks`
  ADD CONSTRAINT `fk_blocks_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`);

--
-- Constraints for table `bonus`
--
ALTER TABLE `bonus`
  ADD CONSTRAINT `fk_bonus_delegator` FOREIGN KEY (`delegator_stake_address`) REFERENCES `delegator` (`stake_address`),
  ADD CONSTRAINT `fk_bonus_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`);

--
-- Constraints for table `gone_delegators`
--
ALTER TABLE `gone_delegators`
  ADD CONSTRAINT `fk_gone delegators_delegator1` FOREIGN KEY (`delegator_stake_address`) REFERENCES `delegator` (`stake_address`),
  ADD CONSTRAINT `fk_gone delegators_epoch1` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`);

--
-- Constraints for table `owner_rewards`
--
ALTER TABLE `owner_rewards`
  ADD CONSTRAINT `fk_owner_rewards_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`),
  ADD CONSTRAINT `fk_owner_rewards_owner` FOREIGN KEY (`owner_stake_address`) REFERENCES `owner` (`stake_address`);

--
-- Constraints for table `pledge`
--
ALTER TABLE `pledge`
  ADD CONSTRAINT `fk_pledge_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`),
  ADD CONSTRAINT `fk_pledge_owner` FOREIGN KEY (`owner_stake_address`) REFERENCES `owner` (`stake_address`);

--
-- Constraints for table `rewards`
--
ALTER TABLE `rewards`
  ADD CONSTRAINT `fk_rewards_delegator` FOREIGN KEY (`delegator_stake_address`) REFERENCES `delegator` (`stake_address`),
  ADD CONSTRAINT `fk_rewards_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`);

--
-- Constraints for table `stake`
--
ALTER TABLE `stake`
  ADD CONSTRAINT `fk_stake_delegator` FOREIGN KEY (`delegator_stake_address`) REFERENCES `delegator` (`stake_address`),
  ADD CONSTRAINT `fk_stake_epoch` FOREIGN KEY (`epoch_epoch_number`) REFERENCES `epoch` (`epoch_number`);
COMMIT;
