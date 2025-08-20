import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../services/data/user.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  private readonly _router = inject(Router);
  private readonly _loginService = inject(LoginService);
  protected readonly userService = inject(UserService);

  readonly defaultSalesQuery = {
    order_by: 'name',
    limit: 100,
    store: 'Crunchyroll',
    condition: 'New'
  };
  readonly defaultSeriesQuery = { order_by: 'title', limit: 20 };
  readonly defaultCollectionQuery = {
    order_by: 'name',
    limit: 100,
    offset: 0,
    collection: 'Collection'
  };

  routeTo(path: string, queryParams = {}) {
    this._router.navigate([path], { queryParams });
  }

  routeToUserPage(path: string, queryParams = {}) {
    this._router.navigate([path], {
      queryParams: {
        ...queryParams,
        username: localStorage.getItem('username')
      }
    });
  }

  callOpenLogin() {
    this._loginService.openLogin().subscribe();
  }
}
