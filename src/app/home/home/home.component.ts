import { NgClass } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { UserService } from '../../services/data/user.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-home',
  imports: [NgClass, ButtonModule, MenubarModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  private readonly _router = inject(Router);
  private readonly _loginService = inject(LoginService);
  protected readonly userService = inject(UserService);

  protected readonly menuItems = computed<MenuItem[]>(() => [
    {
      label: 'Browse Sales',
      icon: 'pi pi-tags',
      path: 'sales',
      queryParams: {
        order_by: 'name',
        limit: 100,
        store: 'Crunchyroll',
        condition: 'New'
      }
    },
    {
      label: 'Browse Series',
      icon: 'pi pi-book',
      path: 'series',
      queryParams: { order_by: 'title', limit: 20 }
    },
    {
      label: 'My Collection',
      icon: 'pi pi-th-large',
      visible: this.userService.userDataIsValid(),
      items: [
        {
          label: 'My Volumes',
          icon: 'pi pi-th-large',
          path: 'collection',
          queryParams: {
            order_by: 'name',
            limit: 100,
            offset: 0,
            collection: 'Collection'
          }
        },
        {
          label: 'My Series',
          icon: 'pi pi-objects-column',
          path: 'series',
          queryParams: { order_by: 'title', limit: 20 }
        }
      ]
    }
  ]);

  // readonly defaultSalesQuery = {
  //   order_by: 'name',
  //   limit: 100,
  //   store: 'Crunchyroll',
  //   condition: 'New'
  // };
  // readonly defaultSeriesQuery = { order_by: 'title', limit: 20 };
  // readonly defaultCollectionQuery = {
  //   order_by: 'name',
  //   limit: 100,
  //   offset: 0,
  //   collection: 'Collection'
  // };

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
