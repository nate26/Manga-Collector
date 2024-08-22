import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionDataService } from '../../services/data/collection-data.service';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { ICollection } from '../../interfaces/iCollection.interface';
import { SearchVolumesComponent } from '../../common/search-volumes/search-volumes.component';
import { IVolume } from '../../interfaces/iVolume.interface';
import { VolumeService } from '../../services/data/volume.service';
import { forkJoin, tap } from 'rxjs';
import { ITheme } from '../../interfaces/iSeries.interface';
import { UserService } from '../../services/data/user.service';
import { TagChipComponent } from '../../common/tag-chip/tag-chip.component';
import { TagListComponent } from '../../common/tag-list/tag-list.component';

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule, SearchVolumesComponent, TagChipComponent, TagListComponent],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    private readonly collectionDataService = inject(CollectionDataService);
    private readonly volumeService = inject(VolumeService);
    private readonly destroy = inject(DestroyRef);
    protected readonly userService = inject(UserService);

    // this.collectionDataService.collectionVolumes$
    volumes = toSignal(this.collectionDataService.collectionVolumes$, { initialValue: [] });
    volumeIDs = computed(() => this.volumes().map(vol => vol.user_collection_data[0].id));
    newVolumes = signal<IVolume[]>([]);
    availableCategories = computed(
        () => this.volumes()
            .map(vol => vol.category)
            .filter((v, i, a) => a.indexOf(v) === i)
    );
    availableMerchants = computed(
        () => this.volumes()
            .map(vol => vol.user_collection_data[0].merchant)
            .filter((v, i, a) => a.indexOf(v) === i)
    );
    availableTags = computed(
        () => this.volumes()
            .map(vol => vol.user_collection_data[0].tags)
            .flat()
            .filter((v, i, a) => a.indexOf(v) === i)
    );

    protected editSwitch = signal(false);
    protected isEditing = computed(() => this.editSwitch() && this.userService.userDataIsValid());

    saveBatch = signal<ICollection[]>([]); // temp cache of save changes
    saved = signal<ICollection[]>([]); // cache of all prior saved records

    deleteBatch = signal<string[]>([]); // temp cache of delete changes
    deleted = signal<string[]>([]); // cache of all prior deleted records

    // consider reactive forms instead of template forms
    filterName = signal<string>('');
    filterCategory = signal<string>('');
    filterVolume = signal<string>('');
    filterCost = signal<string>('');
    filterMerchant = signal<string>('');
    filterPurchaseDate = signal<string>('');
    filterRead = signal<string>('');
    filterGiftToMe = signal<string>('');
    filterTags = signal<string[]>([]);

    // separate filter and saved states for performance
    editedVolumes = computed(() => {
        const vols = this.volumes();
        if (!vols) return [];
        return [
            // add in all new volumes in current batch
            ...this.saveBatch().filter(record => !record.id).map(volume => {
                return {
                    ...this.newVolumes().find(vol => vol.isbn === volume.isbn)!,
                    user_collection_data: [volume],
                    edited: true
                }
            }),
            // add in all new volumes that were previously saved
            ...this.saved().filter(record => this.volumeIDs().indexOf(record.id) === -1).map(volume => {
                return {
                    ...this.newVolumes().find(vol => vol.isbn === volume.isbn)!,
                    user_collection_data: [volume],
                    edited: Boolean(this.saveBatch().find(record => record.id === volume.id))
                }
            }),
            // modify all existing volumes that were edited
            ...vols.map(volume => {
                const editedState = this.saveBatch().find(record => record.id === volume.user_collection_data[0].id);
                const savedState = this.saved().find(record => record.id === volume.user_collection_data[0].id);
                const changed = editedState || savedState;
                if (changed) {
                    return { ...volume, user_collection_data: [changed], edited: Boolean(editedState) };
                }
                return { ...volume, edited: false };
            })
        ].filter(vol => [
            ...this.deleteBatch(),
            ...this.deleted()
        ].indexOf(vol.user_collection_data[0].id ?? '') === -1); // remove deleted records
    });

    filteredVolumes = computed(() => {
        return this.editedVolumes().filter(volume => {
            const record = volume.user_collection_data[0];
            // check name
            return (!this.filterName() || (volume.name ?? '').toLowerCase().includes(this.filterName().toLowerCase()))
                // check category
                && (this.filterCategory() === '' || (volume.category + '') === (this.filterCategory() + ''))
                // check volume
                && (!this.filterVolume() || volume.volume === this.filterVolume())
                // check cost
                && (!this.filterCost() || record.cost.toString() === this.filterCost())
                // check merchant
                && (this.filterMerchant() === '' || (record.merchant + '') === this.filterMerchant())
                // check purchaseDate
                && (!this.filterPurchaseDate() || (record.purchaseDate ?? '').toLowerCase().includes(this.filterPurchaseDate().toLowerCase()))
                // check read
                && (this.filterRead() === '' || record.read === (this.filterRead() === 'YES'))
                // check giftToMe
                && (this.filterGiftToMe() === '' || record.giftToMe === (this.filterGiftToMe() === 'YES'))
                // check tags
                && (this.filterTags().length === 0 ||
                    this.filterTags().some(fTag => record.tags.some(tag => fTag.toLowerCase() === tag.toLowerCase())));
        });
    });

    selectedVol = signal<IVolume | null>(null);

    volumeRowClass = (volume: IVolume & { edited: boolean }) => {
        const classes = [];
        if (this.volumeIsSelected(volume)) classes.push('volume-row-selected');
        else classes.push('volume-row');
        if (volume.edited) classes.push('edited-row');
        return classes.join(' ');
    }

    volumeIsSelected = (volume: IVolume) => {
        const selectedId = this.selectedVol()?.user_collection_data?.[0]?.id ?? this.selectedVol()?.user_collection_data?.[0]?.temp_id;
        const volId = volume.user_collection_data[0].id ?? volume.user_collection_data[0].temp_id;
        return selectedId === volId && selectedId !== undefined;
    }

    parseThemes = (themes: ITheme[]) => themes.map(t => t.theme).join(', ');

    private _batchEdit(batch: ICollection[], record: ICollection) {
        // update batch if record is already in batch
        if (batch.some(b => (b.id ?? b.temp_id) === (record.id ?? record.temp_id))) {
            // update existing if was previously saved
            return batch.map(existingRecord =>
                (existingRecord.id ?? existingRecord.temp_id) === (record.id ?? record.temp_id) ? record : existingRecord);
        }

        if (!record.id && this.saved().some(savedRecord => savedRecord.temp_id === record.temp_id)) {
            // remove from saved if we are re-editing it
            this.saved.update(saved => saved.filter(savedRecord => savedRecord.temp_id !== record.temp_id))
        }

        // add to batch if not already there
        return [...batch, record]
    }

    doEdit(index: number, field: string, value: Event) {
        this.saveBatch.update(batch => {
            const existingRecord = this.filteredVolumes()[index].user_collection_data[0];
            const newValue = this.getEventVal(value);
            let parsedValue;
            if (field === 'cost') parsedValue = parseFloat(newValue);
            else if (field === 'read' || field === 'giftToMe') parsedValue = (<HTMLInputElement>value.target).checked;
            else parsedValue = newValue;
            return this._batchEdit(batch, { ...existingRecord, [field]: parsedValue });
        });
    }

    editTags(index: number, value: string[]): void {
        this.saveBatch.update(batch => {
            return this._batchEdit(
                batch,
                {
                    ...this.filteredVolumes()[index].user_collection_data[0],
                    tags: value
                }
            );
        });
    }

    markForDelete(record: ICollection) {
        if (record.id) {
            this.deleteBatch.update(batch => [...batch, record.id!]);
        }
        else {
            this.saveBatch.update(batch => batch.filter(r => r.temp_id !== record.temp_id));
        }
    }

    save() {
        forkJoin({
            saveResult: this.collectionDataService.saveToCollection(this.saveBatch()).pipe(
                tap({
                    next: (saveResult) => {
                        console.log('The following records were saved: ', this.saveBatch());
                        // merge with existing cache
                        this.saved.update(currSaved => saveResult.reduce((acc, record) => this._batchEdit(acc, record), currSaved));
                        this.saveBatch.set([]);
                    }
                })
            ),
            deleteResult: this.collectionDataService.deleteFromCollection(this.deleteBatch()).pipe(
                tap({
                    next: (deleteResult) => {
                        console.log('The following records were deleted: ', this.deleteBatch());
                        // merge with existing cache
                        this.deleted.update(currDeleted => [...new Set([...currDeleted, ...deleteResult])]);
                        this.deleteBatch.set([]);
                    }
                })
            )
        }).pipe(
            takeUntilDestroyed(this.destroy)
        ).subscribe({
            next: () => {
                this.stopEditing();
                this.editSwitch.set(false);
            }
        });
    }

    stopEditing() {
        this.saveBatch.set([]);
        this.editSwitch.set(false);
    }

    getEventVal(value: Event) {
        const target = (value as InputEvent & {
            target: {
                type: string;
                checked: boolean;
                value: string;
            };
        }).target;
        return target.type === 'checkbox' ? (target.checked ? 'YES' : 'NO') : target.value;
    }

    addVolume(vol: IVolume) {
        const addToBatch = () =>
            this.saveBatch.update(batch => [...batch, this.collectionDataService.buildNewRecord(vol)]);
        if (this.newVolumes().find(v => v.isbn === vol.isbn)) {
            addToBatch();
        }
        else {
            // fetch if not in existing cache
            this.volumeService.queryVolume(vol.isbn).pipe(
                takeUntilDestroyed(this.destroy)
            ).subscribe({
                next: (volume) => {
                    this.newVolumes.update(volumes => [...volumes, volume]);
                    addToBatch();
                },
                error: (err) => {
                    console.error(err);
                    alert('could not get volume data for ' + vol.display_name + 'to add to collection')
                }
            });
        }
    }

    showVolumeDetails(volume: IVolume) {
        if (this.volumeIsSelected(volume)) {
            this.selectedVol.set(null);
        }
        else {
            this.selectedVol.set(volume);
        }
    }

}
