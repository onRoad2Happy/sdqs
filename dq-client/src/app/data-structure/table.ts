import { Attribute } from "./attribute"

export class Table {
    id: number;
    name: string;
    attributes: Attribute[];
    type: string;
    source_id: number;
    source_name: string;
    source_attributes: Attribute[];
}