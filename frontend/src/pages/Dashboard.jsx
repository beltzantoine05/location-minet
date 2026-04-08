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
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
// On récupère des icônes de Lucide-React (inclus par défaut avec shadcn)
import { PlusCircle, Pencil, Trash2 } from "lucide-react"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import apiClient from "@/api/client"
import { useAuth } from "@/context/AuthContext"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"



export default function Dashboard() {
    const navigate = useNavigate()
    const { token } = useAuth()

    // On remplace nos variables en dur par des "States" !
    const [inventory, setInventory] = useState([])
    const [asso, setAsso] = useState(null) // Pour stocker les infos de l'asso co
    const [loading, setLoading] = useState(true)
    const [isAddOpen, setIsAddOpen] = useState(false)
    const [isEditOpen, setIsEditOpen] = useState(false)
    const [itemToEdit, setItemToEdit] = useState(null)

    const [newItem, setNewItem] = useState({
        nom: "",
        description: "",
        prix_location: "",
        caution: "",
    })
    const handleDelete = async (itemId) => {

        if (!window.confirm("Es-tu-sur de vouloir supprimer cet objet ? ")) return

        try {
            await apiClient.delete(`/items/${itemId}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

            setInventory(inventory.filter((item) => item.id !== itemId))

        } catch (error) {
            console.error("Erreur lors de la suppression", error)
            alert("Impossible de supprimer cet objet")
        }
    }

    const handleCreate = async (e) => {
        e.preventDefault()

        try {

            const response = await apiClient.post('/items/', newItem, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

            setInventory([...inventory, response.data])

            setIsAddOpen(false)
            setNewItem({ nom: "", description: "", prix_location: "", caution: "" })

        } catch (error) {
            console.error("Erreur lors de la création de cet objet", error)
            alert("Impossible d'ajouter cet objet. Verifier qu'il ne manque aucun champ !")
        }
    }

    const handleUpdate = async (e) => {
        e.preventDefault(e)

        try {
            const response = await apiClient.put(`/items/${itemToEdit.id}`, itemToEdit, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

            setInventory(inventory.map((item) => (item.id === itemToEdit.id ? response.data : item)))

            setIsEditOpen(false)
            setItemToEdit(null)
        } catch (error) {
            console.error("Erreur lors de la modification", error)
            alert("Impossible de modifier cet objet. Verifier qu'il ne manque aucun champ !")
        }

    }


    // Le fameux videur qui agit à l'ouverture de la page
    useEffect(() => {
        const token = localStorage.getItem("token")

        // Pas de pass VIP ? Dehors !
        if (!token) {
            navigate("/login")
            return
        }

        const verifyAndLoadData = async () => {
            try {
                // 1. On demande poliment au backend : "Qui suis-je ?"
                const responseAsso = await apiClient.get("/associations/me", {
                    headers: {
                        Authorization: `Bearer ${token}` // On montre le pass VIP au serveur
                    }
                })
                setAsso(responseAsso.data)

                // 2. Maintenant qu'on connait notre ID, on demande notre matériel !
                const responseItems = await apiClient.get(`/associations/${responseAsso.data.id}/items`)
                setInventory(responseItems.data)

            } catch (error) {
                // Si le serveur répond 401 (token périmé, ou faux token)
                console.error("Accès refusé ou Token invalide", error)
                localStorage.removeItem("token") // On brûle le faux pass
                navigate("/login") // Dehors !
            } finally {
                setLoading(false)
            }
        }

        verifyAndLoadData()
    }, [navigate])

    // Pendant qu'on papote avec le serveur, on affiche un écran d'attente
    if (loading) {
        return <div className="flex h-[80vh] items-center justify-center">Vérification de la sécurité...</div>
    }

    return (
        <div className="container mx-auto px-4 max-w-7xl py-10">
            {/* L'en-tête dynamique au nom de l'association ! */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Tableau de bord - {asso?.nom}</h1>
                    <p className="text-muted-foreground mt-1">Gère le matériel de ton association, ajoute ou supprime des équipements.</p>
                </div>

                <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
                    {/* Le bouton d'ouverture. shadcn s'occupe de faire le lien. */}
                    <DialogTrigger asChild>
                        <Button className="flex items-center gap-2 shadow-sm transition-transform hover:-translate-y-0.5">
                            <PlusCircle className="h-5 w-5" />
                            Ajouter du matériel
                        </Button>
                    </DialogTrigger>

                    {/* Le contenu de la fameuse fenêtre */}
                    <DialogContent className="sm:max-w-xl">
                        <DialogHeader>
                            <DialogTitle>Ajouter un nouvel équipement</DialogTitle>
                            <DialogDescription>
                                Remplis les détails du matériel proposé à la location.
                            </DialogDescription>
                        </DialogHeader>

                        {/* Le formulaire qui appelle notre fonction à la soumission */}
                        <form onSubmit={handleCreate} className="space-y-4 mt-4">
                            <div className="space-y-2">
                                <Label>Nom de l'équipement</Label>
                                <Input
                                    required
                                    value={newItem.nom}
                                    /* À chaque lettre tapée, on met à jour uniquement "nom" en gardant le reste de l'objet (...newItem) */
                                    onChange={e => setNewItem({ ...newItem, nom: e.target.value })}
                                    placeholder="Ex: Enceinte 1000W"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label>Description</Label>
                                <Textarea
                                    value={newItem.description}
                                    onChange={e => setNewItem({ ...newItem, description: e.target.value })}
                                    placeholder="Accessoires fournis, spécificités..."
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Prix de location (€/j)</Label>
                                    <Input
                                        required
                                        type="number" // Pas de texte !
                                        value={newItem.prix_location}
                                        onChange={e => setNewItem({ ...newItem, prix_location: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Caution (€)</Label>
                                    <Input
                                        required
                                        type="number"
                                        value={newItem.caution}
                                        onChange={e => setNewItem({ ...newItem, caution: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div className="flex justify-end gap-2 pt-4">
                                <Button type="button" variant="outline" onClick={() => setIsAddOpen(false)}>Annuler</Button>
                                <Button type="submit">Ajouter l'équipement</Button>
                            </div>
                        </form>
                    </DialogContent>
                </Dialog>

                <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
                    <DialogContent className="sm:max-w-xl">
                        <DialogHeader>
                            <DialogTitle>Modifier l'équipement</DialogTitle>
                        </DialogHeader>

                        {/* Le formulaire n'est affiché QUE si on détient bien un objet (itemToEdit != null) */}
                        {itemToEdit && (
                            <form onSubmit={handleUpdate} className="space-y-4 mt-4">
                                <div className="space-y-2">
                                    <Label>Nom de l'équipement</Label>
                                    {/* Remarque : on écrase seulement la portion modifiée : {...itemToEdit, nom: ...} */}
                                    <Input required value={itemToEdit.nom} onChange={e => setItemToEdit({ ...itemToEdit, nom: e.target.value })} />
                                </div>

                                <div className="space-y-2">
                                    <Label>Description</Label>
                                    <Textarea value={itemToEdit.description} onChange={e => setItemToEdit({ ...itemToEdit, description: e.target.value })} />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label>Prix de location (€/j)</Label>
                                        <Input required type="number" value={itemToEdit.prix_location} onChange={e => setItemToEdit({ ...itemToEdit, prix_location: e.target.value })} />
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Caution (€)</Label>
                                        <Input required type="number" value={itemToEdit.caution} onChange={e => setItemToEdit({ ...itemToEdit, caution: e.target.value })} />
                                    </div>
                                </div>

                                <div className="flex justify-end gap-2 pt-4">
                                    <Button type="button" variant="outline" onClick={() => setIsEditOpen(false)}>Annuler</Button>
                                    <Button type="submit">Sauvegarder les changements</Button>
                                </div>
                            </form>
                        )}
                    </DialogContent>
                </Dialog>


            </div>

            {/* Le tableau prend maintenant la "vraie" variable inventory de ton State ! */}
            <div className="rounded-md border bg-card animate-in fade-in slide-in-from-bottom-4 duration-700 shadow-sm overflow-hidden">
                <Table>
                    {/* ... Ton <TableHeader> ici ne change pas ... */}
                    <TableHeader className="bg-muted/50">
                        <TableRow>
                            <TableHead>Nom de l'équipement</TableHead>
                            <TableHead>Description</TableHead>
                            <TableHead>Caution</TableHead>
                            <TableHead className="text-right">Tarif</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        {inventory.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-10 text-muted-foreground">
                                    Vous n'avez pas encore de matériel.
                                </TableCell>
                            </TableRow>
                        ) : (
                            inventory.map((item) => (
                                <TableRow key={item.id} className="hover:bg-muted/30 transition-colors">
                                    <TableCell className="font-semibold">{item.nom}</TableCell>

                                    <TableCell className="text-muted-foreground max-w-[200px] truncate">
                                        {item.description}
                                    </TableCell>

                                    <TableCell>
                                        <Badge variant="secondary">{item.caution}€</Badge>
                                    </TableCell>

                                    <TableCell className="text-right font-medium">{item.prix_location}€</TableCell>

                                    <TableCell className="text-right">
                                        <div className="flex items-center justify-end gap-1">
                                            {/* ... Tes boutons d'actions ici ... */}
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-muted-foreground hover:text-primary"
                                                onClick={() => {
                                                    setItemToEdit(item)   // On mémorise quel objet on édite !
                                                    setIsEditOpen(true)   // On ouvre la modale
                                                }}
                                            >
                                                <Pencil className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-muted-foreground hover:text-destructive"
                                                onClick={() => handleDelete(item.id)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    )
}
