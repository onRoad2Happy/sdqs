import { Attribute } from "./attribute"

export class Table {
    id: number;
    name: string;
    summary: Attribute[];
    type: string;
    jobs: string[];
    source_id: number;
    source_name: string;
    source_summary: Attribute[];
    stream_name: string;
}