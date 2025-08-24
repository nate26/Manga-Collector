import { NgClass } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { UserService } from '../../services/data/user.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-home',
  imports: [NgClass, RouterModule, ButtonModule, MenubarModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  #loginService = inject(LoginService);
  #userService = inject(UserService);

  private _currentUser = computed(
    () => this.#userService.userData().username || localStorage.getItem('username')
  );

  userDataIsValid = computed(() => this.#userService.userDataIsValid());

  menuItems = computed<MenuItem[]>(() => [
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
      visible: this.#userService.userDataIsValid(),
      items: [
        {
          label: 'My Volumes',
          icon: 'pi pi-th-large',
          path: 'collection',
          queryParams: {
            order_by: 'name',
            limit: 100,
            offset: 0,
            collection: 'Collection',
            username: this._currentUser()
          }
        },
        {
          label: 'My Series',
          icon: 'pi pi-objects-column',
          path: 'series',
          queryParams: { order_by: 'title', limit: 20, username: this._currentUser() }
        }
      ]
    }
  ]);

  openLogin() {
    this.#loginService.openLogin().subscribe();
  }

  logout() {
    this.#userService.logout();
  }
}
