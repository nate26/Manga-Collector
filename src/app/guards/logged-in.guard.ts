import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { UserService } from '../services/data/user.service';
import { inject } from '@angular/core';
import { LoginService } from '../services/login.service';
import { map, tap } from 'rxjs';

const _navigateToPage = (router: Router, url: string, user_id: string | null) => {
    if (url === '/collection' && user_id) {
        router.navigate(['collection'], { queryParams: { user_id } });
    }
    else if (url === '/series' && user_id) {
        router.navigate(['series'], { queryParams: { user_id } });
    }
}

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = (_route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    const loginService = inject(LoginService);
    const router = inject(Router);
    const isLoggedIn = inject(UserService).userDataIsValid();
    const user_id = localStorage.getItem('user_id');
    const viewOtherUser = (state.url.includes('/collection') || state.url.includes('/series')) && state.url.includes('?user_id=');

    if (isLoggedIn) {
        _navigateToPage(router, state.url, user_id)
    }

    return isLoggedIn || viewOtherUser || loginService.openLogin().pipe(
        tap((userData) => {
            _navigateToPage(router, state.url, userData.user_id)
        }),
        map(() => true)
    );
};
