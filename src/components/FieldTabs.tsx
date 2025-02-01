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
    subFields: ["Computer Science", "Mechanical", "Electrical", "Civil", "Chemical", "Aerospace", "Software", "Biomedical"],
  },
  {
    name: "Medicine",
    subFields: ["MBBS", "Dentistry", "Pharmacy", "Nursing", "Physiotherapy", "Public Health", "Veterinary"],
  },
  {
    name: "Business",
    subFields: ["Finance", "Marketing", "Management", "Economics", "Accounting", "International Business", "Entrepreneurship"],
  },
  {
    name: "Arts",
    subFields: ["Literature", "History", "Philosophy", "Fine Arts", "Music", "Theater", "Film Studies", "Languages"],
  },
  {
    name: "Science",
    subFields: ["Physics", "Chemistry", "Biology", "Mathematics", "Environmental Science", "Astronomy", "Geology"],
  },
  {
    name: "Social Sciences",
    subFields: ["Psychology", "Sociology", "Political Science", "Anthropology", "Geography", "Social Work"],
  },
  {
    name: "Law",
    subFields: ["Criminal Law", "Civil Law", "Corporate Law", "International Law", "Constitutional Law"],
  },
  {
    name: "Technology",
    subFields: ["Information Technology", "Data Science", "Artificial Intelligence", "Cybersecurity", "Cloud Computing"],
  },
  {
    name: "Design",
    subFields: ["Graphic Design", "Industrial Design", "Fashion Design", "Interior Design", "UX/UI Design"],
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