import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { UserService } from '../services/data/user.service';
import { inject } from '@angular/core';
import { LoginService } from '../services/login.service';
import { map, tap } from 'rxjs';

const _navigateToPage = (router: Router, url: string, username: string | null) => {
    if (url === '/collection' && username) {
        router.navigate(['collection'], { queryParams: { username } });
    }
    else if (url === '/series' && username) {
        router.navigate(['series'], { queryParams: { username } });
    }
};

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = (_route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    const loginService = inject(LoginService);
    const router = inject(Router);
    const isLoggedIn = inject(UserService).userDataIsValid();
    const username = localStorage.getItem('username');
    const viewOtherUser = (state.url.includes('/collection') || state.url.includes('/series')) && state.url.includes('?username=');

    if (isLoggedIn) {
        _navigateToPage(router, state.url, username);
    }

    return isLoggedIn || viewOtherUser || loginService.openLogin().pipe(
        tap((userData) => {
            _navigateToPage(router, state.url, userData.username);
        }),
        map(() => true)
    );
};
