import { inject } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivateFn,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { filter, map, tap } from 'rxjs';
import { UserService } from '../../services/data/user.service';
import { LoginService } from '../../services/login.service';

const _navigateToPage = (router: Router, url: string, username: string | null) => {
  if (url === '/collection' && username) {
    router.navigate(['collection'], { queryParams: { username } });
  } else if (url === '/series' && username) {
    router.navigate(['series'], { queryParams: { username } });
  }
};

/**
 * A guard that checks if the user is logged in. If not, the user is redirected to the login page.
 * @returns whether the user is logged in and can route to the requested page
 */
export const loggedInGuard: CanActivateFn = (
  _route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const loginService = inject(LoginService);
  const router = inject(Router);
  const userService = inject(UserService);
  const isLoggedIn = userService.userDataIsValid();
  const username = userService.userData().username;
  const viewOtherUser =
    (state.url.includes('/collection') || state.url.includes('/series')) &&
    state.url.includes('?username=') &&
    Boolean(state.url.split('?username=')[1]);

  if (isLoggedIn && !state.url.includes('?username=')) {
    _navigateToPage(router, state.url, username);
    return true;
  }

  return (
    viewOtherUser ||
    loginService.openLogin().pipe(
      filter(userData => Boolean(userData)),
      tap(userData => {
        _navigateToPage(router, state.url.split('?username=')[0], userData!.username);
      }),
      map(() => true)
    )
  );
};
