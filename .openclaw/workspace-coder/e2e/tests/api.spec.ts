import { test, expect } from '@playwright/test';
import { VoicePixPage } from '../pages/VoicePixPage';

/**
 * API Behavior Tests for VoicePix
 *
 * Tests how the app handles various API error conditions.
 * Uses page.route() to intercept and mock network requests.
 *
 * T40: invalid voice_id → API error toast
 * T41: empty text → validation error toast (before API call)
 * T42: response time within reasonable range
 */

test.describe('API Behavior', () => {
  let vp: VoicePixPage;

  test.beforeEach(async ({ page }) => {
    vp = new VoicePixPage(page);
    await vp.goto();
    // Set a dummy key so the app doesn't block on "no API key"
    await vp.setApiKey('test-gid', 'test-key');
    await vp.tabT2A.click();
  });

  // ── T40: Invalid voice_id → API error ───────────────────────────────────
  test('T40: API call with invalid voice_id shows error toast', async ({ page }) => {
    // Intercept the MiniMax API and return a JSON error
    await page.route('https://api.minimax.io/v1/t2a_v2', async (route) => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({
          base_resp: { status_code: 1003, ret_msg: 'Invalid voice_id' },
        }),
      });
    });

    // Select an invalid voice
    await vp.voicePreset.selectOption('Chinese (Mandarin)_Warm_Girl');
    await vp.typeText('测试文字');

    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/失败|错误|Invalid|fail|error/i);
  });

  // ── T41: Empty text → validation error (before API call) ───────────────
  test('T41: empty text triggers validation error without API call', async ({ page }) => {
    let apiCalled = false;
    await page.route('https://api.minimax.io/v1/t2a_v2', async () => {
      apiCalled = true;
    });

    await vp.clearText();
    await expect(vp.textInput).toHaveValue('');

    await vp.generateBtn.click();

    // Validation should block the API call
    expect(apiCalled).toBe(false);

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/请输入文字|enter text|Please/i);
  });

  // ── T42: API response time within reasonable range ──────────────────────
  test('T42: API call completes within reasonable time (< 15s)', async ({ page }) => {
    // Mock a slow API response
    await page.route('https://api.minimax.io/v1/t2a_v2', async (route) => {
      // 500ms delay before responding
      await page.waitForTimeout(500);
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ base_resp: { status_code: 1003, ret_msg: 'error' } }),
      });
    });

    await vp.typeText('性能测试');
    await vp.generateBtn.click();

    // Measure how long until the error toast appears
    const start = Date.now();
    await vp.waitForToast();
    const elapsed = Date.now() - start;

    // Should complete within 15 seconds (generous upper bound)
    expect(elapsed).toBeLessThan(15000);
    // And obviously more than the 500ms mock delay
    expect(elapsed).toBeGreaterThan(400);
  });

  // ── T43: Network error → error toast shown ───────────────────────────────
  test('T43: network failure shows error toast with meaningful message', async ({ page }) => {
    await page.route('https://api.minimax.io/v1/t2a_v2', async (route) => {
      // Fail the network request entirely
      await route.abort('failed');
    });

    await vp.typeText('网络错误测试');
    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    // Should contain some error indication
    expect(toastText.length).toBeGreaterThan(0);
  });

  // ── T44: 401 unauthorized → specific error toast ─────────────────────────
  test('T44: 401 unauthorized response shows correct error toast', async ({ page }) => {
    await page.route('https://api.minimax.io/v1/t2a_v2', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ base_resp: { status_code: 1002, ret_msg: 'Unauthorized' } }),
      });
    });

    await vp.typeText('认证失败测试');
    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/失败|错误|Unauthorized|认证/i);
  });

  // ── T45: rate-limit / 429 → error toast ────────────────────────────────
  test('T45: 429 rate-limit response shows error toast', async ({ page }) => {
    await page.route('https://api.minimax.io/v1/t2a_v2', async (route) => {
      await route.fulfill({
        status: 429,
        contentType: 'application/json',
        body: JSON.stringify({ base_resp: { status_code: 1005, ret_msg: 'Rate limit exceeded' } }),
      });
    });

    await vp.typeText('频率限制测试');
    await vp.generateBtn.click();

    const toastText = await vp.waitForToast();
    expect(toastText.length).toBeGreaterThan(0);
  });
});
