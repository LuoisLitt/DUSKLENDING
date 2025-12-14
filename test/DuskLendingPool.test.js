const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DuskLendingPool", function () {
  let duskToken, usdtToken, lendingPool;
  let owner, user1, user2, liquidator;
  let initialDuskPrice;

  beforeEach(async function () {
    [owner, user1, user2, liquidator] = await ethers.getSigners();

    // Deploy mock tokens
    const MockDUSK = await ethers.getContractFactory("MockDUSK");
    duskToken = await MockDUSK.deploy();
    await duskToken.waitForDeployment();

    const MockUSDT = await ethers.getContractFactory("MockUSDT");
    usdtToken = await MockUSDT.deploy();
    await usdtToken.waitForDeployment();

    // Deploy lending pool with initial DUSK price of $0.50
    initialDuskPrice = 50000000; // $0.50 with 8 decimals
    const DuskLendingPool = await ethers.getContractFactory("DuskLendingPool");
    lendingPool = await DuskLendingPool.deploy(
      await duskToken.getAddress(),
      await usdtToken.getAddress(),
      initialDuskPrice
    );
    await lendingPool.waitForDeployment();

    // Supply initial USDT liquidity to the pool
    const initialLiquidity = ethers.parseUnits("100000", 6);
    await usdtToken.approve(await lendingPool.getAddress(), initialLiquidity);
    await lendingPool.supplyUsdt(initialLiquidity);

    // Give users some tokens
    await duskToken.transfer(user1.address, ethers.parseEther("1000"));
    await duskToken.transfer(user2.address, ethers.parseEther("1000"));
    await usdtToken.transfer(user1.address, ethers.parseUnits("10000", 6));
    await usdtToken.transfer(liquidator.address, ethers.parseUnits("10000", 6));
  });

  describe("Deployment", function () {
    it("Should set the correct token addresses", async function () {
      expect(await lendingPool.duskToken()).to.equal(await duskToken.getAddress());
      expect(await lendingPool.usdtToken()).to.equal(await usdtToken.getAddress());
    });

    it("Should set the correct initial price", async function () {
      expect(await lendingPool.duskPriceUSD()).to.equal(initialDuskPrice);
    });

    it("Should have initial USDT liquidity", async function () {
      expect(await lendingPool.totalUsdtLiquidity()).to.equal(ethers.parseUnits("100000", 6));
    });
  });

  describe("Depositing DUSK", function () {
    it("Should allow users to deposit DUSK", async function () {
      const depositAmount = ethers.parseEther("100");

      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);

      const userData = await lendingPool.users(user1.address);
      expect(userData.duskCollateral).to.equal(depositAmount);
      expect(await lendingPool.totalDuskDeposited()).to.equal(depositAmount);
    });

    it("Should emit DuskDeposited event", async function () {
      const depositAmount = ethers.parseEther("100");

      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await expect(lendingPool.connect(user1).depositDusk(depositAmount))
        .to.emit(lendingPool, "DuskDeposited")
        .withArgs(user1.address, depositAmount);
    });

    it("Should revert when depositing 0", async function () {
      await expect(lendingPool.connect(user1).depositDusk(0)).to.be.revertedWith(
        "Amount must be > 0"
      );
    });
  });

  describe("Borrowing USDT", function () {
    beforeEach(async function () {
      // User deposits 100 DUSK as collateral
      const depositAmount = ethers.parseEther("100");
      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);
    });

    it("Should allow users to borrow USDT", async function () {
      // With 100 DUSK at $0.50, user can borrow up to $50 / 1.5 = $33.33 USDT
      const borrowAmount = ethers.parseUnits("30", 6);

      const initialBalance = await usdtToken.balanceOf(user1.address);
      await lendingPool.connect(user1).borrowUsdt(borrowAmount);

      const userData = await lendingPool.users(user1.address);
      expect(userData.usdtBorrowed).to.equal(borrowAmount);
      expect(await usdtToken.balanceOf(user1.address)).to.equal(initialBalance + borrowAmount);
    });

    it("Should revert when borrowing too much", async function () {
      // Try to borrow more than allowed by collateral
      const borrowAmount = ethers.parseUnits("50", 6);

      await expect(lendingPool.connect(user1).borrowUsdt(borrowAmount)).to.be.revertedWith(
        "Insufficient collateral"
      );
    });

    it("Should emit UsdtBorrowed event", async function () {
      const borrowAmount = ethers.parseUnits("30", 6);

      await expect(lendingPool.connect(user1).borrowUsdt(borrowAmount))
        .to.emit(lendingPool, "UsdtBorrowed")
        .withArgs(user1.address, borrowAmount);
    });
  });

  describe("Repaying USDT", function () {
    beforeEach(async function () {
      // User deposits and borrows
      const depositAmount = ethers.parseEther("100");
      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);

      const borrowAmount = ethers.parseUnits("30", 6);
      await lendingPool.connect(user1).borrowUsdt(borrowAmount);
    });

    it("Should allow users to repay USDT", async function () {
      const repayAmount = ethers.parseUnits("10", 6);

      await usdtToken.connect(user1).approve(await lendingPool.getAddress(), repayAmount);
      await lendingPool.connect(user1).repayUsdt(repayAmount);

      const userData = await lendingPool.users(user1.address);
      expect(userData.usdtBorrowed).to.equal(ethers.parseUnits("20", 6));
    });

    it("Should emit UsdtRepaid event", async function () {
      const repayAmount = ethers.parseUnits("10", 6);

      await usdtToken.connect(user1).approve(await lendingPool.getAddress(), repayAmount);
      await expect(lendingPool.connect(user1).repayUsdt(repayAmount))
        .to.emit(lendingPool, "UsdtRepaid")
        .withArgs(user1.address, repayAmount);
    });
  });

  describe("Withdrawing DUSK", function () {
    beforeEach(async function () {
      // User deposits DUSK
      const depositAmount = ethers.parseEther("100");
      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);
    });

    it("Should allow users to withdraw DUSK when no debt", async function () {
      const withdrawAmount = ethers.parseEther("50");

      const initialBalance = await duskToken.balanceOf(user1.address);
      await lendingPool.connect(user1).withdrawDusk(withdrawAmount);

      expect(await duskToken.balanceOf(user1.address)).to.equal(initialBalance + withdrawAmount);

      const userData = await lendingPool.users(user1.address);
      expect(userData.duskCollateral).to.equal(ethers.parseEther("50"));
    });

    it("Should revert when trying to withdraw too much with debt", async function () {
      // Borrow first
      await lendingPool.connect(user1).borrowUsdt(ethers.parseUnits("30", 6));

      // Try to withdraw all collateral
      await expect(
        lendingPool.connect(user1).withdrawDusk(ethers.parseEther("100"))
      ).to.be.revertedWith("Insufficient collateral ratio");
    });
  });

  describe("Liquidation", function () {
    beforeEach(async function () {
      // User deposits and borrows at max
      const depositAmount = ethers.parseEther("100");
      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);

      const borrowAmount = ethers.parseUnits("33", 6);
      await lendingPool.connect(user1).borrowUsdt(borrowAmount);
    });

    it("Should allow liquidation when position is unhealthy", async function () {
      // Drop DUSK price to make position unhealthy
      await lendingPool.updateDuskPrice(20000000); // $0.20

      // Position should now be unhealthy
      expect(await lendingPool.getHealthFactor(user1.address)).to.be.lt(ethers.parseEther("1"));

      // Liquidate
      const repayAmount = ethers.parseUnits("10", 6);
      await usdtToken.connect(liquidator).approve(await lendingPool.getAddress(), repayAmount);

      const initialDuskBalance = await duskToken.balanceOf(liquidator.address);
      await lendingPool.connect(liquidator).liquidate(user1.address, repayAmount);

      // Liquidator should receive DUSK with bonus
      expect(await duskToken.balanceOf(liquidator.address)).to.be.gt(initialDuskBalance);
    });

    it("Should revert liquidation of healthy position", async function () {
      const repayAmount = ethers.parseUnits("10", 6);
      await usdtToken.connect(liquidator).approve(await lendingPool.getAddress(), repayAmount);

      await expect(
        lendingPool.connect(liquidator).liquidate(user1.address, repayAmount)
      ).to.be.revertedWith("Position is healthy");
    });
  });

  describe("View Functions", function () {
    beforeEach(async function () {
      const depositAmount = ethers.parseEther("100");
      await duskToken.connect(user1).approve(await lendingPool.getAddress(), depositAmount);
      await lendingPool.connect(user1).depositDusk(depositAmount);
    });

    it("Should return correct max borrow amount", async function () {
      const maxBorrow = await lendingPool.getMaxBorrowAmount(user1.address);
      // 100 DUSK * $0.50 / 1.5 = $33.33 USDT
      expect(maxBorrow).to.be.closeTo(ethers.parseUnits("33.33", 6), ethers.parseUnits("0.01", 6));
    });

    it("Should return infinite health factor when no debt", async function () {
      const healthFactor = await lendingPool.getHealthFactor(user1.address);
      expect(healthFactor).to.equal(ethers.MaxUint256);
    });
  });

  describe("Admin Functions", function () {
    it("Should allow owner to update price", async function () {
      const newPrice = 100000000; // $1.00
      await lendingPool.updateDuskPrice(newPrice);
      expect(await lendingPool.duskPriceUSD()).to.equal(newPrice);
    });

    it("Should revert when non-owner tries to update price", async function () {
      await expect(
        lendingPool.connect(user1).updateDuskPrice(100000000)
      ).to.be.revertedWithCustomError(lendingPool, "OwnableUnauthorizedAccount");
    });

    it("Should allow owner to update interest rates", async function () {
      await lendingPool.updateInterestRates(600, 400);
      expect(await lendingPool.borrowAPR()).to.equal(600);
      expect(await lendingPool.supplyAPR()).to.equal(400);
    });
  });
});
