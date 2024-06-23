import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { UserService } from '../services/data/user.service';
import { inject } from '@angular/core';

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = (_route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    const router = inject(Router);
    console.log('test')
    const isLoggedIn = inject(UserService).isLoggedIn();
    console.log('okok guard', isLoggedIn)

    if (state.url === '/login' && !isLoggedIn) {
        return true;
    }

    if (!isLoggedIn) {
        router.navigate(['login']);
    }
    else if (state.url === '/login') {
        router.navigate(['collection']);
    }

    return isLoggedIn;
};
