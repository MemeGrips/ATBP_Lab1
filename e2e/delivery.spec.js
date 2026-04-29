const { test, expect } = require('@playwright/test');
const { DeliveryPage } = require('./pages/DeliveryPage');

test.describe('Вариант 13: Доставка', () => {
    let deliveryPage;

    test.beforeEach(async ({ page }) => {
        deliveryPage = new DeliveryPage(page);
        await deliveryPage.navigate();
    });

    test('Успешный расчет: Трасса без пробок', async () => {
        await deliveryPage.calculate(100, 50, 'трасса', '0');
        const result = await deliveryPage.getResult();
        expect(result).toContain('2 часов');
    });

    test('Логика: В городе с пробками время больше', async ({ page }) => {
        // 1. Считаем БЕЗ пробок
        await deliveryPage.calculate(60, 60, 'город', '0');
        const text1 = await deliveryPage.getResult();
        const match1 = text1.match(/\d+\.\d+|\d+/);
        const timeWithoutTraffic = parseFloat(match1[0]);

        // Перезагружаем, чтобы очистить состояние
        await page.reload();
        deliveryPage = new DeliveryPage(page);

        // 2. Считаем С пробками (Москва - 7)
        await deliveryPage.calculate(60, 60, 'город', '7');
        const text2 = await deliveryPage.getResult();
        const match2 = text2.match(/\d+\.\d+|\d+/);
        const timeWithTraffic = parseFloat(match2[0]);

        expect(timeWithTraffic).toBeGreaterThan(timeWithoutTraffic);
    });

    const negativeCases = [
        { dist: -10, speed: 50, terr: 'трасса', error: 'Расстояние должно быть положительным' },
        { dist: 100, speed: 200, terr: 'трасса', error: 'Скорость не может превышать 150 км/ч' },
        { dist: 100, speed: 70, terr: 'город', error: 'В городе скорость не может превышать 60 км/ч' },
        { dist: 0, speed: 50, terr: 'трасса', error: 'Расстояние должно быть положительным' }
    ];

    for (const data of negativeCases) {
        test(`Ошибка при значении ${data.dist !== 100 ? data.dist : data.speed}: ${data.error}`, async () => {
            await deliveryPage.calculate(data.dist, data.speed, data.terr);
            const error = await deliveryPage.getError();
            expect(error).toContain(data.error);
        });
    }
});