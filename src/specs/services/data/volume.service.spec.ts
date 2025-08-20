import { TestBed } from '@angular/core/testing';
import { VolumeService } from '../../../app/services/data/volume.service';
import { Apollo, QueryRef } from 'apollo-angular';
import { UserService } from '../../../app/services/data/user.service';
import { of } from 'rxjs';
import { ApolloError, ApolloQueryResult, OperationVariables } from '@apollo/client/core';
import { IGQLAllRecord, IGQLGetRecord } from '../../../app/interfaces/iGQLRequests.interface';
import { IVolume } from '../../../app/interfaces/iVolume.interface';
import { signal } from '@angular/core';

describe('VolumeService', () => {
    let service: VolumeService;
    let apolloMock: jasmine.SpyObj<Apollo>;
    let userServiceMock: jasmine.SpyObj<UserService>;

    beforeEach(() => {
        apolloMock = jasmine.createSpyObj(['watchQuery']);
        apolloMock.watchQuery.and.returnValue({
            valueChanges: of()
        } as unknown as QueryRef<unknown, OperationVariables>);
        userServiceMock = jasmine.createSpyObj([], ['userData']);
    });

    describe('VOLUMES_BASIC_QUERY Success', () => {

        beforeEach(() => {
            apolloMock.watchQuery.and.returnValue({
                valueChanges: of({
                    data: {
                        all_records: {
                            records: [
                                {
                                    isbn: '1234567890',
                                    series: 'Test Series',
                                    display_name: 'Test Volume',
                                    volume: '1',
                                    primary_cover_image_url: 'https://test.com/image.jpg'
                                },
                                {
                                    isbn: '0987654321',
                                    series: 'Test Series 2',
                                    display_name: 'Test Volume 2',
                                    volume: '2',
                                    primary_cover_image_url: 'https://test.com/image2.jpg'
                                }
                            ] as IVolume[],
                        },
                        success: true,
                        errors: []
                    },
                    loading: false,
                    networkStatus: 7
                } as ApolloQueryResult<IGQLAllRecord>)
            } as unknown as QueryRef<unknown, OperationVariables>);
            TestBed.configureTestingModule({
                providers: [
                    { provide: Apollo, useValue: apolloMock },
                    { provide: UserService, useValue: userServiceMock }
                ]
            });
            service = TestBed.inject(VolumeService);
        });

        it('should get all volumes with basic fields from GQL', () => {
            let result: IVolume[] = [];
            service.volumesBasic$.subscribe({
                next: volumes => result = volumes,
                error: fail
            });
            expect(result).toEqual([
                {
                    isbn: '1234567890',
                    series: 'Test Series',
                    display_name: 'Test Volume',
                    volume: '1',
                    primary_cover_image_url: 'https://test.com/image.jpg'
                },
                {
                    isbn: '0987654321',
                    series: 'Test Series 2',
                    display_name: 'Test Volume 2',
                    volume: '2',
                    primary_cover_image_url: 'https://test.com/image2.jpg'
                }
            ] as IVolume[]);
            expect(apolloMock.watchQuery).toHaveBeenCalledOnceWith({
                query: service['VOLUMES_BASIC_QUERY'],
                variables: { user_id: null }
            });
        });

    });

    describe('VOLUMES_BASIC_QUERY Error', () => {

        beforeEach(() => {
            apolloMock.watchQuery.and.returnValue({
                valueChanges: of({
                    data: {
                        all_records: {
                            records: [],
                        },
                        success: false,
                        errors: ['Test Error']
                    },
                    loading: false,
                    networkStatus: 7,
                    error: new Error('Test Error') as ApolloError
                } as ApolloQueryResult<IGQLAllRecord>)
            } as unknown as QueryRef<unknown, OperationVariables>);
            TestBed.configureTestingModule({
                providers: [
                    { provide: Apollo, useValue: apolloMock },
                    { provide: UserService, useValue: userServiceMock }
                ]
            });
            service = TestBed.inject(VolumeService);
        });

        it('should throw an error when GQL query fails', () => {
            let result: Error = new Error();
            service.volumesBasic$.subscribe({
                next: fail,
                error: err => result = err
            });
            expect(result.message).toEqual('Could not get all volumes because Test Error');
        });

    });

    describe('SINGLE_VOLUME_QUERY', () => {

        beforeEach(() => {
            userServiceMock = {
                ...jasmine.createSpyObj([], ['userData']),
                userData: signal({
                    username: 'natevin',
                    email: '123test@gmail.com',
                    user_id: '12345678',
                    profile: {
                        picture: null,
                        banner: null,
                        color: null,
                        theme: null
                    },
                    personal_stores: [],
                    authentication: {
                        token: '123token',
                        refresh_token: '123refresh',
                        expiration: (Date.now() / 1000) + ''
                    }
                })
            };
            TestBed.configureTestingModule({
                providers: [
                    { provide: Apollo, useValue: apolloMock },
                    { provide: UserService, useValue: userServiceMock }
                ]
            });
            service = TestBed.inject(VolumeService);
        });

        it('should get a single volume with all fields from GQL', () => {
            apolloMock.watchQuery.and.returnValue({
                valueChanges: of({
                    data: {
                        get_record: {
                            record: {
                                isbn: '1234567890',
                                brand: 'Test Brand',
                                series: 'Test Series',
                                series_id: '123',
                                display_name: 'Test Volume'
                            } as IVolume,
                        },
                        success: true,
                        errors: []
                    },
                    loading: false,
                    networkStatus: 7
                } as ApolloQueryResult<IGQLGetRecord>)
            } as unknown as QueryRef<unknown, OperationVariables>);
            let result: IVolume = {} as IVolume;
            service.queryVolume('1234567890').subscribe({
                next: volume => result = volume,
                error: fail
            });
            expect(apolloMock.watchQuery).toHaveBeenCalledWith({
                query: service['SINGLE_VOLUME_QUERY'],
                variables: { isbn: '1234567890', user_id: '12345678' }
            });
            expect(result).toEqual({
                isbn: '1234567890',
                brand: 'Test Brand',
                series: 'Test Series',
                series_id: '123',
                display_name: 'Test Volume'
            } as IVolume);
        });

        it('should throw an error when GQL query fails', () => {
            apolloMock.watchQuery.and.returnValue({
                valueChanges: of({
                    data: {
                        get_record: {
                            record: null,
                        },
                        success: false,
                        errors: ['Test Error']
                    },
                    loading: false,
                    networkStatus: 7,
                    error: new Error('Test Error') as ApolloError
                } as ApolloQueryResult<IGQLGetRecord>)
            } as unknown as QueryRef<unknown, OperationVariables>);
            let result: Error = new Error();
            service.queryVolume('1234567890').subscribe({
                next: fail,
                error: err => result = err
            });
            expect(result.message).toEqual('Could not get all volumes because Test Error');
        });

    });
});
