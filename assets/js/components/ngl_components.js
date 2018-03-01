/**
 * Created by abradley on 01/03/2018.
 */
import { Stage, concatStructures, Selection } from 'ngl';
import React from 'react';


export class NGLView extends React.Component {


    constructor(props) {
        super(props);
        // Create NGL Stage object
        this.div_id = "viewport";
        this.focus_var = 95;
        this.height = "600px";
        this.interval = 10000
        this.show_mol = this.show_mol.bind(this);
    }

    componentDidMount(){
        this.stage = new Stage(this.div_id);
        // Handle window resizing
        window.addEventListener("resize", function (event) {
            this.stage.handleResize();
        }, false);
        this.show_mol();
        setInterval(this.show_mol,
            this.interval)
    }

    show_mol() {
        const MOL_URL = "/viewer/mol_from_pk/"
        if (this.props.mol_dict) {
            const prot_url = this.props.mol_dict["prot_id"]
            const mol_id = this.props.mol_dict["mol_id"]
            const mol_url = MOL_URL + mol_id.toString() + "/"
            const object_name = mol_id.toString()
            NProgress.start();
            Promise.all([
                this.stage.loadFile(prot_url, {ext: "pdb"}),
                this.stage.loadFile(mol_url, {ext: "sdf"})]
            ).then(function (ol) {
                var cs = concatStructures(
                    "concat",
                    ol[0].structure.getView(new Selection("not ligand")),
                    ol[1].structure.getView(new Selection(""))
                )
                cs.path = object_name
                var comp = this.stage.addComponentFromObject(cs)
                comp.addRepresentation("cartoon")
                comp.addRepresentation("contact", {
                    masterModelIndex: 0,
                    weakHydrogenBond: true,
                    maxHbondDonPlaneAngle: 35,
                    sele: "/0 or /1"
                })
                comp.addRepresentation("licorice", {
                    sele: "ligand and /1",
                    multipleBond: "offset"
                })
                comp.addRepresentation("line", {
                    sele: "/0"
                })
                comp.autoView("ligand");
                NProgress.done();
                this.stage.setFocus(this.focus_var);
            })
        }
    }
    render(){

        return <div style={{height: this.height}} id={this.div_id}></div>

    }
}