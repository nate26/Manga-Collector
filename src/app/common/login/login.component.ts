import { DIALOG_DATA, DialogRef } from '@angular/cdk/dialog';
import { AsyncPipe, NgTemplateOutlet } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators
} from '@angular/forms';
import { debounceTime, iif, map } from 'rxjs';
import {
  LOGIN_PATH_CONTEXT,
  SIGNUP_PATH_CONTEXT,
  UserService
} from '../../services/data/user.service';
import { UserData } from '../../services/data/user.type';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, AsyncPipe, NgTemplateOutlet],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private readonly _userService = inject(UserService);
  private readonly _destroyRef = inject(DestroyRef);
  private readonly _dialogRef = inject(DialogRef<UserData, LoginComponent>);

  protected readonly pathContext = signal(inject<typeof LOGIN_PATH_CONTEXT>(DIALOG_DATA));
  protected readonly isPathLogin = computed(
    () => this.pathContext().path === LOGIN_PATH_CONTEXT.path
  );

  //#region Form
  protected readonly userForm = new FormGroup({
    email: new FormControl('', [
      Validators.required,
      // Validators.email
      Validators.pattern(
        "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)" +
          '*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\' +
          '[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])' +
          '?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])' +
          '|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]' +
          '|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-' +
          '\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\\])'
      )
    ]),
    username: new FormControl<string | null>(null, [
      (control: AbstractControl): ValidationErrors | null =>
        !this.isPathLogin() ? Validators.required(control) : null,
      Validators.minLength(3)
    ]),
    password: new FormControl('', [
      Validators.required,
      Validators.pattern(
        '(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!#^~%*?&,.<>"\'\\;:{\\}\\[\\]\\|\\+' +
          '\\-\\=\\_\\)\\(\\)\\`\\/\\\\\\]])[A-Za-z0-9d$@].{8,}'
      )
    ])
  });
  //#endregion

  protected readonly loginError = signal('');

  //#region Validators
  protected readonly emailError$ = this.userForm.valueChanges.pipe(
    debounceTime(500),
    map(() => {
      if (!this.userForm.controls.email.touched || this.userForm.controls.email.valid) {
        return '';
      }
      if (this.userForm.controls.email.errors?.['required']) {
        return 'An email address is required.';
      }
      return 'Please provide a valid email address.';
    })
  );

  protected readonly usernameError$ = this.userForm.valueChanges.pipe(
    debounceTime(500),
    map(() => {
      if (!this.userForm.controls.username.touched || this.userForm.controls.username.valid) {
        return '';
      }
      if (this.userForm.controls.username.errors?.['required']) {
        return 'A username is required.';
      }
      return 'Your username must be at least 3 characters.';
    })
  );

  protected readonly passwordError$ = this.userForm.valueChanges.pipe(
    debounceTime(500),
    map(() => {
      const value = this.userForm.controls.password.value;
      if (
        !value ||
        !this.userForm.controls.password.touched ||
        this.userForm.controls.password.valid
      ) {
        return '';
      }
      if (!RegExp('.*[A-Z].*').test(value)) {
        return 'Password must contain at least one capital letter.';
      }
      if (!RegExp('.*[0-9].*').test(value)) {
        return 'Password must contain at least one number.';
      }
      if (!RegExp('.{8,}').test(value)) {
        return 'Password must be at least 8 characters long.';
      }
      return 'Password must contain a special character.';
    })
  );
  //#endregion

  /**
   * User login or sign up to get the user's auth token.
   * This is parameterized by the current path (login or sign-up).
   * If the login is successful, the user is redirected to the collection page.
   */
  protected login(): void {
    if (this.userForm.invalid) return;

    const { username, password, email } = this.userForm.value;

    iif(
      () => this.isPathLogin(),
      this._userService.login(email, password),
      this._userService.signUp(email, username, password)
    )
      .pipe(takeUntilDestroyed(this._destroyRef))
      .subscribe({
        next: userData => {
          this.loginError.set('');
          this._dialogRef.close(userData);
        },
        error: (err: HttpErrorResponse) => {
          this.loginError.set(err.error.message);
        }
      });
  }

  protected switchPath() {
    if (this.isPathLogin()) {
      this.pathContext.set(SIGNUP_PATH_CONTEXT);
    } else {
      this.pathContext.set(LOGIN_PATH_CONTEXT);
      this.userForm.controls.username.setValue(null);
    }
  }

  protected closeLogin() {
    this._dialogRef.close();
  }
}
