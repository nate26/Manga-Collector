import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { UserService } from '../services/data/user.service';
import { inject } from '@angular/core';
import { LoginService } from '../services/login.service';

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = (_route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    const router = inject(Router);
    const loginService = inject(LoginService);
    const isLoggedIn = inject(UserService).isLoggedIn();
    const user_id = localStorage.getItem('user_id');
    const viewOtherUser = (state.url.includes('/collection') || state.url.includes('/series')) && state.url.includes('?user_id=');

    if (!isLoggedIn && state.url === '/login') {
        return true;
    }

    if (isLoggedIn) {
        if (state.url === '/login' || state.url === '/collection' && user_id) {
            router.navigate(['collection'], { queryParams: { user_id } });
        }
        else if (state.url === '/series' && user_id) {
            router.navigate(['series'], { queryParams: { user_id } });
        }
    }

    return isLoggedIn || viewOtherUser || loginService.openLogin();
};
