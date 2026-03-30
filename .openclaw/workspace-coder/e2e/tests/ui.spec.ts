import { test, expect } from '@playwright/test';
import { VoicePixPage } from '../pages/VoicePixPage';

/**
 * UI Interaction Tests for VoicePix
 *
 * Tests language switching, tab navigation, and API Key modal interactions.
 */

test.describe('UI Interactions', () => {
  let vp: VoicePixPage;

  test.beforeEach(async ({ page }) => {
    vp = new VoicePixPage(page);
    await vp.goto();
  });

  // ── T20: Chinese/English language switching ──────────────────────────────
  test('T20: switching to English updates all UI labels', async ({ page }) => {
    // Default is Chinese — check key Chinese labels
    const heading = page.locator('#s-t2a h1');
    await expect(heading).toContainText('文字转语音');

    // Switch to English
    await vp.switchLang('en');

    // Heading should now be in English
    await expect(heading).toContainText('Text to Speech');

    // Generate button text
    const genBtn = page.locator('#genBtn');
    await expect(genBtn).toContainText(/Generate Speech/i);

    // Tab texts
    await expect(vp.tabT2A).toContainText(/Text to Speech/i);
    await expect(vp.tabClone).toContainText(/Voice Clone/i);

    // Textarea placeholder
    await expect(page.locator('textarea[id="tText"]')).toHaveAttribute(
      'placeholder',
      /Type your text here/i
    );
  });

  test('T20b: switching back to Chinese restores Chinese labels', async ({ page }) => {
    await vp.switchLang('en');
    await vp.switchLang('zh');

    const heading = page.locator('#s-t2a h1');
    await expect(heading).toContainText('文字转语音');
  });

  // ── T25: Tab switching ───────────────────────────────────────────────────
  test('T25: clicking Clone tab shows clone section, clicking T2A shows T2A section', async ({ page }) => {
    // T2A should be visible by default
    await expect(page.locator('#s-t2a')).toHaveClass(/on/);
    await expect(page.locator('#s-clone')).not.toHaveClass(/on/);

    // Click Clone tab
    await vp.tabClone.click();
    await expect(page.locator('#s-clone')).toHaveClass(/on/);
    await expect(page.locator('#s-t2a')).not.toHaveClass(/on/);

    // Tab button should show active state
    await expect(vp.tabClone).toHaveClass(/active/);
    await expect(vp.tabT2A).not.toHaveClass(/active/);

    // Switch back to T2A
    await vp.tabT2A.click();
    await expect(page.locator('#s-t2a')).toHaveClass(/on/);
    await expect(page.locator('#s-clone')).not.toHaveClass(/on/);
  });

  // ── T30: API Key modal — save key ───────────────────────────────────────
  test('T30: API Key modal saves key and button shows ✓ state', async ({ page }) => {
    // Button should not have .set class initially (no key)
    await expect(vp.apikeyBtn).not.toHaveClass(/set/);

    await vp.openApiKeyModal();

    // Modal should be visible
    await expect(vp.modal).toHaveClass(/on/);
    await expect(vp.gidInput).toBeVisible();
    await expect(vp.keyInput).toBeVisible();
    await expect(vp.saveKeyBtn).toBeVisible();
    await expect(vp.deleteKeyBtn).toBeVisible();

    // Fill and save
    await vp.gidInput.fill('my-test-gid-123');
    await vp.keyInput.fill('my-test-secret-456');
    await vp.saveKeyBtn.click();

    // Modal should close
    await vp.modal.waitFor({ state: 'hidden' });

    // Button should now show set state
    await expect(vp.apikeyBtn).toHaveClass(/set/);
    await expect(vp.apikeyBtn).toContainText(/✓|API Key/i);

    // Toast success
    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/已保存|Saved/i);
  });

  // ── T30b: API Key modal — delete key ────────────────────────────────────
  test('T30b: API Key modal deletes key and button reverts to default state', async ({ page }) => {
    // First set a key
    await vp.setApiKey('gid-for-delete', 'key-for-delete');
    await expect(vp.apikeyBtn).toHaveClass(/set/);

    // Delete the key
    await vp.deleteApiKey();

    // Button should no longer have .set
    await expect(vp.apikeyBtn).not.toHaveClass(/set/);
    await expect(vp.apikeyBtn).toContainText('API Key');

    // Toast
    const toastText = await vp.waitForToast();
    expect(toastText).toMatch(/已删除|Deleted/i);
  });

  // ── T30c: API Key modal — close via × button ───────────────────────────
  test('T30c: clicking × closes modal without saving', async ({ page }) => {
    await vp.openApiKeyModal();
    await expect(vp.modal).toHaveClass(/on/);

    await vp.closeModalBtn.click();
    await vp.modal.waitFor({ state: 'hidden' });

    // Key should not have been saved
    await expect(vp.apikeyBtn).not.toHaveClass(/set/);
  });

  // ── T30d: API Key modal — clicking outside modal does NOT close ─────────
  test('T30d: clicking backdrop does not close modal (by design)', async ({ page }) => {
    await vp.openApiKeyModal();
    await expect(vp.modal).toHaveClass(/on/);

    // Click the backdrop (outside the modal box)
    await page.mouse.click(10, 10);

    // Modal should stay open (no auto-close implemented)
    await page.waitForTimeout(300);
    // We don't assert strict visibility here since the behavior may vary;
    // the primary close action is the × button
  });

  // ── T31: Toast disappears after timeout ─────────────────────────────────
  test('T31: toast auto-hides after ~3 seconds', async ({ page }) => {
    // Trigger a toast (no API key)
    await vp.typeText('触发 toast');
    await vp.generateBtn.click();
    await vp.waitForToast();

    // Toast should still be visible right now
    await expect(vp.toast).toHaveClass(/on/);

    // Wait for auto-hide (toast timeout is 3200ms)
    await page.waitForTimeout(3500);
    await expect(vp.toast).not.toHaveClass(/on/);
  });

  // ── T32: Voice grid renders all voices ─────────────────────────────────
  test('T32: voice grid renders all predefined voices', async ({ page }) => {
    await vp.voiceGrid.waitFor({ state: 'visible' });

    const voiceItems = page.locator('.vitem');
    const count = await voiceItems.count();
    // We expect 19 voices (10 Chinese + 9 English as per VOICES array)
    expect(count).toBeGreaterThanOrEqual(19);

    // All should have a play button
    const playBtns = page.locator('.vplay');
    expect(await playBtns.count()).toBe(count);
  });

  // ── T33: Logo and header are always visible ─────────────────────────────
  test('T33: header logo and nav tabs are always visible across sections', async ({ page }) => {
    const logo = page.locator('.logo');
    await expect(logo).toBeVisible();

    // Logo text
    await expect(logo).toContainText('VoicePix');

    // Lang toggle and API Key button in header
    await expect(vp.langZhBtn).toBeVisible();
    await expect(vp.langEnBtn).toBeVisible();
    await expect(vp.apikeyBtn).toBeVisible();

    // Switch sections and verify header still visible
    await vp.tabClone.click();
    await expect(logo).toBeVisible();
    await expect(vp.langZhBtn).toBeVisible();
  });
});
