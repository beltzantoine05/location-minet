import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
// On récupère des icônes de Lucide-React (inclus par défaut avec shadcn)
import { PlusCircle, Pencil, Trash2 } from "lucide-react"

// Données fictives d'inventaire
const inventory = [
    { id: "1", name: "Enceinte Sono 1000W", category: "Son", status: "Disponible", condition: "Bon", price: "20€/j" },
    { id: "2", name: "Tireuse à bière", category: "Événementiel", status: "En location", condition: "Très bon", price: "15€/j" },
    { id: "3", name: "Câble RJ45 20m", category: "Réseau", status: "Disponible", condition: "Usé", price: "Gratuit" },
]

export default function Dashboard() {
    return (
        <div className="container mx-auto px-4 max-w-7xl py-10">

            {/* L'en-tête du Dashboard avec le bouton d'ajout */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Tableau de bord de l'Asso</h1>
                    <p className="text-muted-foreground mt-1">Gère le matériel de ton association, ajoute ou supprime des équipements.</p>
                </div>

                <Button className="flex items-center gap-2 shadow-sm transition-transform hover:-translate-y-0.5">
                    <PlusCircle className="h-5 w-5" />
                    Ajouter du matériel
                </Button>
            </div>

            {/* Le fameux tableau d'inventaire */}
            <div className="rounded-md border bg-card animate-in fade-in slide-in-from-bottom-4 duration-700 shadow-sm overflow-hidden">
                <Table>

                    <TableHeader className="bg-muted/50">
                        <TableRow>
                            <TableHead>Nom de l'équipement</TableHead>
                            <TableHead>Catégorie</TableHead>
                            <TableHead>Statut</TableHead>
                            <TableHead>État</TableHead>
                            <TableHead className="text-right">Tarif</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        {inventory.map((item) => (
                            <TableRow key={item.id} className="hover:bg-muted/30 transition-colors">
                                <TableCell className="font-semibold">{item.name}</TableCell>
                                <TableCell className="text-muted-foreground">{item.category}</TableCell>
                                <TableCell>
                                    {/* Le "Badge" met en forme le statut dynamiquement */}
                                    <Badge variant={item.status === "Disponible" ? "default" : "secondary"}>
                                        {item.status}
                                    </Badge>
                                </TableCell>
                                <TableCell>{item.condition}</TableCell>
                                <TableCell className="text-right font-medium">{item.price}</TableCell>

                                {/* Actions (Éditer / Supprimer) */}
                                <TableCell className="text-right">
                                    <div className="flex items-center justify-end gap-1">
                                        <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-primary">
                                            <Pencil className="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive">
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

        </div>
    )
}
