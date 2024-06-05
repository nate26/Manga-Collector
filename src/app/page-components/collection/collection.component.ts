import { Component, DestroyRef, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionDataService } from '../../services/data/collection-data.service';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop'
import { ICollection } from '../../interfaces/iCollection.interface';
import { SearchVolumesComponent } from '../../common/search-volumes/search-volumes.component';
import { IVolume } from '../../interfaces/iVolume.interface';
import { VolumeService } from '../../services/data/volume.service';

interface TextEvent extends Event {
    target: EventTarget & { value: string };
}

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule, SearchVolumesComponent],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    volumes = toSignal(this.collectionDataService.collectionVolumes$, { initialValue: [] });
    newVolumes = signal<IVolume[]>([]);

    editing = signal(false);

    saveBatch = signal<ICollection[]>([]); // temp cache of changes
    saved = signal<ICollection[]>([]); // cache of all prior saved records

    // consider reactive forms instead of template forms
    filterName = signal<string>('');
    filterCategory = signal<string>('');
    filterVolume = signal<string>('');
    filterCost = signal<string>('');
    filterMerchant = signal<string>('');
    filterPurchaseDate = signal<string>('');
    filterRead = signal<string>('');
    filterGiftToMe = signal<string>('');
    filterTags = signal<string>('');

    // separate filter and saved states for performance
    editedVolumes = computed(() => {
        const vols = this.volumes();
        if (!vols) return [];
        return [
            // add in all new volumes
            ...this.saveBatch().filter(record => !record.id).map(record => ({
                ...this.newVolumes().find(vol => vol.isbn === record.isbn)!,
                user_collection_data: [record],
                edited: true
            })),
            ...vols.map(volume => {
                const editedState = this.saveBatch().find(record => record.id === volume.user_collection_data[0].id);
                const savedState = this.saved().find(record => record.id === volume.user_collection_data[0].id);
                const changed = editedState || savedState;
                if (changed) {
                    return { ...volume, user_collection_data: [changed], edited: Boolean(editedState) };
                }
                return { ...volume, edited: false };
            })
        ];
    });

    filteredVolumes = computed(() => {
        return this.editedVolumes().filter(volume => {
            const record = volume.user_collection_data[0];
            // check name
            return (!this.filterName() || (volume.name ?? '').toLowerCase().includes(this.filterName().toLowerCase()))
                // check category
                && (this.filterCategory() === '' || volume.category === this.filterCategory())
                // check volume
                && (!this.filterVolume() || volume.volume === this.filterVolume())
                // check cost
                && (!this.filterCost() || record.cost.toString() === this.filterCost())
                // check merchant
                && (this.filterMerchant() === '' || record.merchant === this.filterMerchant())
                // check purchaseDate
                && (!this.filterPurchaseDate() || (record.purchaseDate ?? '').toLowerCase().includes(this.filterPurchaseDate().toLowerCase()))
                // check read
                && (this.filterRead() === '' || record.read === (this.filterRead() === 'YES'))
                // check giftToMe
                && (this.filterGiftToMe() === '' || record.giftToMe === (this.filterGiftToMe() === 'YES'))
                // check tags
                && (!this.filterTags() || record.tags.join(',').toLowerCase().includes(this.filterTags().toLowerCase()));
        });
    });

    constructor(
        private collectionDataService: CollectionDataService,
        private volumeService: VolumeService,
        private destroy: DestroyRef) { }

    private _batchEdit(batch: ICollection[], record: ICollection) {
        // update batch if record is already in batch
        if (batch.some(b => (b.id ?? b.temp_id) === (record.id ?? record.temp_id))) {
            // update existing if was previously saved
            return batch.map(existingRecord =>
                (existingRecord.id ?? existingRecord.temp_id) === (record.id ?? record.temp_id) ? record : existingRecord);
        }

        // add to batch if not already there
        return [...batch, record]
    }

    edit(index: number, field: string, value: Event) {
        this.saveBatch.update(batch => {

            // get existing record
            const record = this.filteredVolumes()[index].user_collection_data[0];

            // parse new value
            const eventVal = this.getEventVal(value);
            let parsedValue;
            if (field === 'tags') parsedValue = eventVal ? eventVal.split(',').map(t => t.trim()) : [];
            else if (field === 'cost') parsedValue = parseFloat(eventVal);
            else if (field === 'read' || field === 'giftToMe') parsedValue = (<HTMLInputElement>value.target).checked;
            else parsedValue = eventVal;

            return this._batchEdit(batch, { ...record, [field]: parsedValue });
        })
    }

    save() {
        this.collectionDataService.saveToCollection(this.saveBatch()).pipe(
            takeUntilDestroyed(this.destroy)
        ).subscribe({
            next: (result) => {
                if (result.data?.modify_collection.success) {
                    console.log('The following records were saved: ', this.saveBatch());
                    this.saved.update(batch => this.saveBatch().reduce((acc, record) => this._batchEdit(acc, record), batch));
                    this.stopEditing();
                }
                else {
                    console.error('could not save data... ', result)
                }
            }
        });
    }

    stopEditing() {
        this.saveBatch.set([]);
        this.editing.set(false);
    }

    getEventVal(value: Event) {
        return (<TextEvent>value).target.value;
    }

    addVolume(vol: IVolume) {
        this.volumeService.queryVolume(vol.isbn).pipe(
            takeUntilDestroyed(this.destroy)
        ).subscribe({
            next: (volume) => {
                this.newVolumes.update(volumes => [...volumes, volume]);
                this.saveBatch.update(batch => [...batch, this.collectionDataService.buildNewRecord(vol)]);
            }
        });
    }

}
