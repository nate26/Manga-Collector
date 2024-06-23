import { CanActivateFn, Router } from '@angular/router';
import { UserService } from '../services/data/user.service';
import { inject } from '@angular/core';

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = () => {
    const router = inject(Router);
    const isLoggedIn = inject(UserService).isLoggedIn();
    if (!isLoggedIn) {
        router.navigate(['login']);
    }
    return isLoggedIn;
};
