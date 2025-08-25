import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of } from 'rxjs';
import { HomeComponent } from '../../../app/components/header/header.component';
import { UserService } from '../../../app/services/data/user.service';
import { LoginService } from '../../../app/services/login.service';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;

  let routerMock: jasmine.SpyObj<Router>;
  let loginServiceMock: jasmine.SpyObj<LoginService>;
  let userServiceMock: jasmine.SpyObj<UserService>;

  beforeEach(async () => {
    routerMock = jasmine.createSpyObj(['navigateByUrl', 'navigate']);
    loginServiceMock = jasmine.createSpyObj(['openLogin']);
    userServiceMock = jasmine.createSpyObj(['userDataIsValid', 'logout']);
    await TestBed.configureTestingModule({
      imports: [HomeComponent],
      providers: [
        { provide: Router, useValue: routerMock },
        { provide: LoginService, useValue: loginServiceMock },
        { provide: UserService, useValue: userServiceMock }
      ]
    }).compileComponents();

    window.localStorage.clear();
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should route to the provided path', () => {
    component.routeTo('test');
    expect(routerMock.navigateByUrl).toHaveBeenCalledOnceWith('test');
  });

  it('should route to the provided path for a user', () => {
    window.localStorage.setItem('username', 'user-test');
    component.routeToUserPage('test');
    expect(routerMock.navigate).toHaveBeenCalledOnceWith(['test'], {
      queryParams: { username: 'user-test' }
    });
  });

  it('should call the openLogin method', () => {
    loginServiceMock.openLogin.and.returnValue(of());
    component.callOpenLogin();
    expect(loginServiceMock.openLogin).toHaveBeenCalledTimes(1);
  });

  it('should show my series and my volumes if user is valid', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#my-series')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('#my-collection')).toBeTruthy();
  });

  it('should not show my series and my volumes if user is not valid', () => {
    userServiceMock.userDataIsValid.and.returnValue(false);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#my-series')).toBeFalsy();
    expect(fixture.nativeElement.querySelector('#my-collection')).toBeFalsy();
  });

  it('should route to user page when clicking on my series', () => {
    const routeToUserPageSpy = spyOn(component, 'routeToUserPage');
    userServiceMock.userDataIsValid.and.returnValue(true);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('#my-series').click();
    expect(routeToUserPageSpy).toHaveBeenCalledOnceWith('series');
  });

  it('should route to user page when clicking on my collection', () => {
    const routeToUserPageSpy = spyOn(component, 'routeToUserPage');
    userServiceMock.userDataIsValid.and.returnValue(true);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('#my-collection').click();
    expect(routeToUserPageSpy).toHaveBeenCalledOnceWith('collection');
  });

  it('should only show Sign Out if user is valid', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#sign-out')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('#log-in')).toBeFalsy();
  });

  it('should call logout when clicking on Sign Out', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('#sign-out').click();
    expect(userServiceMock.logout).toHaveBeenCalledTimes(1);
  });

  it('should only show Login if user is not valid', () => {
    userServiceMock.userDataIsValid.and.returnValue(false);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#log-in')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('#sign-out')).toBeFalsy();
  });

  it('should call callOpenLogin when clicking on Login', () => {
    const callOpenLoginSpy = spyOn(component, 'callOpenLogin');
    userServiceMock.userDataIsValid.and.returnValue(false);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('#log-in').click();
    expect(callOpenLoginSpy).toHaveBeenCalledTimes(1);
  });
});
