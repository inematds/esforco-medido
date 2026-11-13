import io, json, os, subprocess, sys, tempfile, unittest
from contextlib import redirect_stdout

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
import relatorio as R  # noqa: E402

FIX = os.path.join(AQUI, "fixture", "fable-low-intervalos.jsonl")


def ev_bash(cmd):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": cmd}}]}}


class BashTipo(unittest.TestCase):
    def test_suite(self):
        self.assertEqual(R.bash_tipo("python3 -m unittest discover -s tests"), {"suite", "conferencia"})

    def test_leitura(self):
        self.assertEqual(R.bash_tipo("cat intervalos.py; ls tests"), {"leitura"})

    def test_escrita_python_so_escreve(self):
        self.assertEqual(R.bash_tipo("python3 - <<'EOF'\nopen('a.py','w').write('x')\nEOF"), {"escrita"})

    def test_escrita_e_confere(self):
        t = R.bash_tipo("python3 - <<'EOF'\nopen('a.py','w').write('x')\nEOF\npython3 -c 'import a'")
        self.assertIn("escrita", t); self.assertIn("conferencia", t)

    def test_confere_adhoc(self):
        self.assertEqual(R.bash_tipo("python3 -c 'from carrinho import total; print(total([]))'"), {"conferencia"})

    def test_sed_i(self):
        self.assertIn("escrita", R.bash_tipo("sed -i 's/>/>=/' frete.py"))


class Contar(unittest.TestCase):
    def test_fixture_real(self):
        c, r = R.contar(R.ler_jsonl(FIX))
        self.assertEqual(c["ferramentas"], 5)
        self.assertEqual(c["por_ferramenta"], {"Read": 2, "Glob": 1, "Edit": 1, "Bash": 1})
        self.assertEqual(c["edicoes"], 1)
        self.assertEqual(c["suite_rodada"], 1)
        self.assertEqual(r["num_turns"], 6)

    def test_releitura_pos_edicao(self):
        ev = [{"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {}},
            {"type": "tool_use", "name": "Edit", "input": {}},
            {"type": "tool_use", "name": "Read", "input": {}}]}}]
        c, _ = R.contar(ev)
        self.assertEqual((c["leituras"], c["releituras_pos_edicao"]), (2, 1))

    def test_erros_e_subagente(self):
        ev = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Task", "input": {}}]}},
              {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": True}]}}]
        c, _ = R.contar(ev)
        self.assertEqual((c["subagentes"], c["erros_ferramenta"]), (1, 1))

    def test_rascunho_fora_do_projeto(self):
        ev = [{"type": "system", "subtype": "init", "cwd": "/x/run/p"},
              {"type": "assistant", "message": {"content": [
                  {"type": "tool_use", "name": "Write", "input": {"file_path": "/x/scratch/sondar.py"}},
                  {"type": "tool_use", "name": "Write", "input": {"file_path": "/x/run/p/carrinho.py"}},
                  {"type": "tool_use", "name": "Bash", "input": {"command": "D=$(mktemp -d); cat > $D/t.py <<E\nE\npython3 $D/t.py"}}]}}]
        c, _ = R.contar(ev)
        self.assertEqual((c["edicoes"], c["rascunhos"], c["conferencias"]), (1, 2, 1))

    def test_texto_final(self):
        ev = [{"type": "assistant", "message": {"content": [{"type": "text", "text": "um"}]}},
              {"type": "assistant", "message": {"content": [{"type": "text", "text": "Pronto. Quer que eu adicione testes?"}]}}]
        c, _ = R.contar(ev)
        self.assertTrue(R.OFERTA.search(c["texto_final"]))

    def test_linha_quebrada_ignorada(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write('{"type":"x"}\nnão é json\n')
        self.assertEqual(len(R.ler_jsonl(f.name)), 1)


class Rodada(unittest.TestCase):
    def test_rodada_e_juntar(self):
        with tempfile.TemporaryDirectory() as d:
            chk = os.path.join(d, "c.txt"); open(chk, "w").write("  falhou x\nNOTA 9/12\n")
            buf = io.StringIO()
            with redirect_stdout(buf):
                R.main(["rodada", FIX, "--id", "fable-low-1", "--modelo", "fable", "--esforco", "low", "--checar", chk])
            linha = json.loads(buf.getvalue())
            self.assertEqual(linha["nota"], "9/12")
            self.assertEqual(linha["modelo_real"], "claude-fable-5-2")
            self.assertGreater(linha["tokens_pensamento"], 0)
            outra = dict(linha, id="opus-high-1", modelo_pedido="opus", esforco="high", modelo_real="claude-fable-5-2")
            open(os.path.join(d, "rodadas.jsonl"), "w").write(json.dumps(linha) + "\n" + json.dumps(outra) + "\n")
            R.main(["juntar", d])
            md = open(os.path.join(d, "RESULTADO.md")).read()
            self.assertIn("| fable-low-1 | claude-fable-5-2 | 9/12 |", md)
            self.assertIn("claude-fable-5-2 ⚠", md)   # pediu opus, rodou fable
            self.assertEqual(len(json.load(open(os.path.join(d, "resultado.json")))), 2)

    def test_refazer_e_linha(self):
        with tempfile.TemporaryDirectory() as d:
            import shutil
            shutil.copy(FIX, os.path.join(d, "fable-low-1.jsonl"))
            open(os.path.join(d, "fable-low-1.checar.txt"), "w").write("NOTA 16/16\n")
            velha = {"id": "fable-low-1", "modelo_pedido": "fable", "esforco": "low", "rc": 0, "tempo_s": 1, "edicoes": 99}
            open(os.path.join(d, "rodadas.jsonl"), "w").write(json.dumps(velha) + "\n")
            R.main(["refazer", d])
            nova = json.loads(open(os.path.join(d, "rodadas.jsonl")).read())
            self.assertEqual((nova["edicoes"], nova["nota"]), (1, "16/16"))
            buf = io.StringIO()
            with redirect_stdout(buf):
                R.main(["linha", os.path.join(d, "rodadas.jsonl")])
            self.assertIn("fable-low-1: nota 16/16", buf.getvalue())

    def test_sem_checar(self):
        self.assertEqual(R.nota(None), (None, None))


class Checadores(unittest.TestCase):
    """Os checadores ocultos dão nota baixa para o código original (a tarefa não vem resolvida)."""
    def _nota(self, tarefa):
        p = subprocess.run([sys.executable, os.path.join(RAIZ, "tarefas", tarefa, "oculto", "checar.py"),
                            os.path.join(RAIZ, "tarefas", tarefa, "projeto")], capture_output=True, text=True)
        return p.returncode, p.stdout.strip().splitlines()[-1]

    def test_carrinho_original(self):
        rc, ultima = self._nota("carrinho")
        self.assertEqual((rc, ultima), (1, "NOTA 5/12"))

    def test_calendario_original(self):
        rc, ultima = self._nota("calendario")
        self.assertEqual((rc, ultima), (1, "NOTA 0/20"))

    def test_intervalos_original(self):
        rc, ultima = self._nota("intervalos")
        self.assertEqual(rc, 1); self.assertTrue(ultima.startswith("NOTA 0/"))


if __name__ == "__main__":
    unittest.main()
