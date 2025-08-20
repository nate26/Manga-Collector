import { Dialog } from '@angular/cdk/dialog';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginComponent } from '../home/login/login.component';
import { UserData } from '../interfaces/iUserData.type';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  readonly #dialog = inject(Dialog);

  /**
   * Open the login dialog.
   * @returns An observable that emits whether the user is logged in
   * when the dialog is closed.
   */
  openLogin(): Observable<UserData | undefined> {
    return this.#dialog.open<UserData>(LoginComponent, {
      data: {
        path: '/login',
        name: 'Login'
      },
      disableClose: true
    }).closed;
  }
}
