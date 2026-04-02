import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter, CardDescription } from "@/components/ui/card"
import { Link } from "react-router-dom"

// On importe notre logo décoratif
import Logo from "@/assets/minet_light.png"

export default function Login() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">

            {/* Petit rappel de la marque au-dessus de la carte */}
            <Link to="/" className="mb-6 flex flex-col items-center gap-2 group">
                <img src={Logo} alt="Logo MiNET" className="w-14 h-14 transition-transform group-hover:scale-110" />
                <span className="font-extrabold text-xl tracking-tight text-primary">LocationMinet</span>
            </Link>

            {/* La carte qui englobe le formulaire */}
            <Card className="w-full max-w-md shadow-lg border-muted/60">

                <CardHeader className="space-y-1 text-center">
                    <CardTitle className="text-2xl font-bold tracking-tight">
                        Connexion Asso
                    </CardTitle>
                    {/* CardDescription permet d'avoir du texte automatiquement grisé proprement */}
                    <CardDescription className="text-sm">
                        Connecte-toi pour gérer le matériel de ton association.
                    </CardDescription>
                </CardHeader>

                <CardContent>
                    {/* Le formulaire (sans action pour l'instant vu qu'on n'a pas de backend) */}
                    <form className="space-y-6">

                        {/* Champ Email */}
                        <div className="space-y-2">
                            <Label htmlFor="email">Adresse email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="asso@bde.minet.net"
                            />
                        </div>

                        {/* Champ Mot de Passe */}
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <Label htmlFor="password">Mot de passe</Label>
                                <a href="#" className="text-xs text-primary hover:underline">
                                    Oublié ?
                                </a>
                            </div>
                            <Input
                                id="password"
                                type="password"
                            />
                        </div>

                        {/* Le Bouton de Validation */}
                        <Button type="button" className="w-full font-semibold">
                            Se connecter
                        </Button>
                    </form>
                </CardContent>

                {/* Le bas de carte, avec une couleur légèrement différente pour détacher l'info */}
                <CardFooter className="flex flex-col items-center justify-center gap-2 border-t pt-6 bg-muted/10 rounded-b-lg">
                    <p className="text-sm text-muted-foreground">
                        Ton association n'est pas encore inscrite ?
                    </p>
                    <Link to="/contact" className="text-sm font-semibold text-primary hover:underline">
                        Fais une demande d'accès
                    </Link>
                </CardFooter>
            </Card>
        </div>
    )
}

