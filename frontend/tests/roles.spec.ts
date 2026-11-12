import { expect, test } from "@playwright/test"

import { createUser } from "./utils/privateApi"
import { randomEmail, randomPassword } from "./utils/random"
import { logInUser } from "./utils/user"

test.describe("Role-aware navigation", () => {
  test.use({ storageState: { cookies: [], origins: [] } })

  test("member is redirected away from users and metrics", async ({ page }) => {
    const email = randomEmail()
    const password = randomPassword()
    await createUser({ email, password })
    await logInUser(page, email, password)

    await page.goto("/admin")
    await expect(page).toHaveURL("/")

    await page.goto("/metrics")
    await expect(page).toHaveURL("/")
  })
})
