class DeliveryPage {
    constructor(page) {
        this.page = page;
        this.distanceInput = '#distance';
        this.speedInput = '#speed';
        this.terrainSelect = '#terrainType';
        this.trafficSelect = '#trafficScore';
        this.submitButton = '#calculateBtn';
        this.resultText = '#resultText';
        this.errorText = '#errorText';
    }

    async navigate() {
        await this.page.goto('http://localhost:5000');
    }

    async calculate(distance, speed, terrain, traffic = "0") {
        await this.page.fill(this.distanceInput, '');
        await this.page.fill(this.distanceInput, distance.toString());
        await this.page.fill(this.speedInput, '');
        await this.page.fill(this.speedInput, speed.toString());

        await this.page.selectOption(this.terrainSelect, terrain);
        await this.page.selectOption(this.trafficSelect, traffic);
        await this.page.click(this.submitButton);
    }

    async getResult() {
        const locator = this.page.locator(this.resultText);
        await locator.waitFor({ state: 'visible' });
        await expect(locator).not.toHaveText('', { timeout: 5000 });
        return await locator.innerText();
    }

    async getError() {
        const locator = this.page.locator(this.errorText);
        await locator.waitFor({ state: 'visible' });
        await expect(locator).not.toHaveText('', { timeout: 5000 });
        return await locator.innerText();
    }
}

const { expect } = require('@playwright/test');
module.exports = { DeliveryPage };