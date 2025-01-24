import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ChevronDown } from "lucide-react";

const fields = [
  {
    name: "Engineering",
    subFields: ["Computer Science", "Mechanical", "Electrical", "Civil"],
  },
  {
    name: "Medicine",
    subFields: ["MBBS", "Dentistry", "Pharmacy", "Nursing"],
  },
  {
    name: "Business",
    subFields: ["Finance", "Marketing", "Management", "Economics"],
  },
  {
    name: "Arts",
    subFields: ["Literature", "History", "Philosophy", "Fine Arts"],
  },
  {
    name: "Science",
    subFields: ["Physics", "Chemistry", "Biology", "Mathematics"],
  },
];

export const FieldTabs = () => {
  return (
    <div className="w-full overflow-x-auto">
      <div className="flex gap-2 min-w-max p-2">
        {fields.map((field) => (
          <DropdownMenu key={field.name}>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="flex items-center gap-2">
                {field.name}
                <ChevronDown className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              {field.subFields.map((subField) => (
                <DropdownMenuItem key={subField}>{subField}</DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        ))}
      </div>
    </div>
  );
};