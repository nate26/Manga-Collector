import { TestBed } from '@angular/core/testing';
import { LoginService } from '../../app/services/login.service';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { LoginComponent } from '../../app/home/login/login.component';
import { Subject } from 'rxjs';

describe('LoginService', () => {
  let service: LoginService;
  let matDialogMock: jasmine.SpyObj<MatDialog>;

  beforeEach(() => {
    matDialogMock = jasmine.createSpyObj(['open']);
    TestBed.configureTestingModule({
      providers: [{ provide: MatDialog, useValue: matDialogMock }]
    });
    service = TestBed.inject(LoginService);
  });

  it('should open login window', () => {
    const ref: jasmine.SpyObj<MatDialogRef<LoginComponent>> = jasmine.createSpyObj(['afterClosed']);
    const onClose = new Subject<void>();
    ref.afterClosed.and.returnValue(onClose);
    matDialogMock.open.and.returnValue(ref);
    const sub = service.openLogin().subscribe({
      error: fail
    });
    expect(matDialogMock.open).toHaveBeenCalledOnceWith(LoginComponent, {
      data: {
        path: '/login',
        name: 'Login'
      },
      disableClose: true
    });
    expect(sub.closed).toBe(false);
    onClose.complete();
    expect(sub.closed).toBe(true);
  });
});
