import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CollectionComponent } from '../../../app/page-components/collection/collection.component';
import { CollectionDataService } from '../../../app/services/data/collection-data.service';
import { DestroyRef } from '@angular/core';
import { VolumeService } from '../../../app/services/data/volume.service';
import { UserService } from '../../../app/services/data/user.service';
import { of } from 'rxjs';

describe('CollectionComponent', () => {
    let component: CollectionComponent;
    let fixture: ComponentFixture<CollectionComponent>;

    let collectionDataServiceMock: jasmine.SpyObj<CollectionDataService>;
    let volumeServiceMock: jasmine.SpyObj<VolumeService>;
    let destroyRefMock: jasmine.SpyObj<DestroyRef>;
    let userServiceMock: jasmine.SpyObj<UserService>;

    beforeEach(async () => {
        collectionDataServiceMock = {
            ...jasmine.createSpyObj(['saveToCollection', 'deleteFromCollection',
                'buildNewRecord']),
            collectionVolumes$: of([])
        };
        volumeServiceMock = jasmine.createSpyObj(['queryVolume']);
        destroyRefMock = jasmine.createSpyObj(['onDestroy']);
        userServiceMock = jasmine.createSpyObj(['canUserEdit', 'userDataIsValid']);

        await TestBed.configureTestingModule({
            imports: [CollectionComponent],
            providers: [
                { provide: CollectionDataService, useValue: collectionDataServiceMock },
                { provide: VolumeService, useValue: volumeServiceMock },
                { provide: DestroyRef, useValue: destroyRefMock },
                { provide: UserService, useValue: userServiceMock }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(CollectionComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
