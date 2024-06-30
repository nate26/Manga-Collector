import { Injectable, inject } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { LoginComponent } from '../home/login/login.component';

@Injectable({
    providedIn: 'root'
})
export class LoginService {

    private readonly _matDialog = inject(MatDialog);

    constructor() { }

    /**
     * Open the login dialog.
     * @returns An observable that emits whether the user is logged in
     * when the dialog is closed.
     */
    openLogin(): Observable<boolean> {
        return this._matDialog.open(LoginComponent, {
            data: {
                path: '/login',
                name: 'Login'
            },
            disableClose: true
        }).afterClosed();
    }

}
