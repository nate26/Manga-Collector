import { TestBed } from '@angular/core/testing';
import { SeriesDataService } from '../../../app/services/data/series-data.service';
import { Apollo } from 'apollo-angular';
import { of } from 'rxjs';
import { UserService } from '../../../app/services/data/user.service';

describe('SeriesDataService', () => {
    let service: SeriesDataService;

    let apolloMock: jasmine.SpyObj<Apollo>;
    let userServiceMock: jasmine.SpyObj<UserService>;

    const MOCK_USER_DATA = {
        username: 'test',
        email: 'test@gmail.com',
        user_id: '1',
        profile: {
            picture: 'picture',
            banner: 'banner',
            color: 'color',
            theme: 'theme'
        },
        personal_stores: ['store'],
        authentication: {
            token: 'token',
            expiration: 'expiration',
            refresh_token: 'refresh_token'
        }
    };

    beforeEach(() => {
        apolloMock = jasmine.createSpyObj(['watchQuery']);
        userServiceMock = {
            ...jasmine.createSpyObj([], ['userData']),
            userIdFromRoute$: of(MOCK_USER_DATA)
        };
        TestBed.configureTestingModule({
            providers: [
                { provide: Apollo, useValue: apolloMock },
                { provide: UserService, useValue: userServiceMock }
            ]
        });
        service = TestBed.inject(SeriesDataService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
